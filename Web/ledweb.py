import tornado.web
import tornado.ioloop
import threading
import os
import re
import json

import sys
sys.path.append('..')
from app_globals import controller, config, writer_types
from led.pattern import Bemis100Pattern
from led.beat import BeatPatternRMS, BeatPattern
from led.graphEq import GraphEqPattern
from led.wave import WavePattern
from led.new_wave import NewWavePattern
from led.mix import MixPattern
from led.bemis100 import Bemis100Writer
from led.utils import find_patterns
from led.lcm_viewer import LCMWriter

def get_preview_path(pat):
    return os.path.join(config['build_dir'], 'previews', re.sub(r'\.[^.]*$', '.gif', pat))


def get_thumb_path(pat):
    return os.path.join(config['build_dir'], 'thumbs', pat)


def format_for_viewer(pat):
    return {'name': pat,
            'preview': get_preview_path(pat),
            'thumb': get_thumb_path(pat)}


class Home(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html", title="Bemis100")


class PatternGroups(tornado.web.RequestHandler):
    def get(self):
        patterns = find_patterns(config['pattern_dir'])
        self.write(json.dumps({'pattern_groups': patterns}))


class Status(tornado.web.RequestHandler):
    def get(self):
        status = {}
        if controller.current is None:
            status['current'] = None
        else:
            status['current'] = format_for_viewer(controller.current.name)

        status['queue'] = []
        # for p in controller.queue:
        #     if isinstance(p, MixPattern):
        #         status['queue'].append(format_for_viewer(re.sub(r'\/[^\/]*', '/_mix.png', p.name)))
        #     else:
        #         status['queue'].append(format_for_viewer(p.name))

        status['playing'] = controller.is_playing()
        # status['autoplay'] = controller.autoplay
        self.write(json.dumps({'controller_status': status}))


class AddPattern(tornado.web.RequestHandler):
    def get(self):
        params = self.request.arguments
        print params
        if 'pattern' in params or 'beatpattern' in params \
                or 'grapheqpattern' in params or 'folder' in params:
            p = None
            track_beat = params['beat'][0] == 'true'
            graph_eq = 'grapheq' in params
            if 'pattern' in params:
                pattern_name = params['pattern'][0]
                if pattern_name.startswith("Specials"):
                    if "new_wave" in pattern_name:
                        p = NewWavePattern(num_lights=config['num_lights'])
                    elif "wave" in pattern_name:
                        p = WavePattern(num_lights=config['num_lights'])
                else:
                    pattern_path = os.path.join(config['pattern_dir'], pattern_name)
                    if os.path.exists(pattern_path):
                        p = Bemis100Pattern(pattern_path, config['num_lights'])
            elif 'folder' in params:
                folder = params['folder'][0]
                folder = re.sub(r'^/*', '', folder)
                pattern_path = os.path.join(config['pattern_dir'], folder)
                print "folder", folder
                print "pattern path", pattern_path
                pattern_name = folder
                p = MixPattern(pattern_path, config['num_lights'])

            if p is not None:
                if track_beat:
                    p = BeatPattern(p)
                elif graph_eq:
                    p = GraphEqPattern(p)

                if 'num_times' in params:
                    n = int(params['num_times'])
                else:
                    n = -1

                controller.add_pattern(p, n, name=pattern_name)
                print "Added pattern:", pattern_name
            else:
                print "Invalid pattern name:", pattern_name
        print "done"
        self.write(json.dumps(dict(success=True)))

class Pause(tornado.web.RequestHandler):
    def get(self):
        print "pause"
        controller.pause()
        self.write(json.dumps(dict(success=True)))

class Play(tornado.web.RequestHandler):
    def get(self):
        print "play"
        controller.play()
        self.write(json.dumps(dict(success=True)))

class AutoplayOn(tornado.web.RequestHandler):
    def get(self):
        controller.autoplay = True
        self.write(json.dumps(dict(success=True)))

class AutoplayOff(tornado.web.RequestHandler):
    def get(self):
        controller.autoplay = False
        self.write(json.dumps(dict(success=True)))

class Next(tornado.web.RequestHandler):
    def get(self):
        print "next"
        controller.next()
        self.write(json.dumps(dict(success=True)))

class GetWriters(tornado.web.RequestHandler):
    def get(self):
        writer_list = []
        for writer in controller.writers:
            writer_list.append('%s on device %s' % (writer.__class__.__name__, writer.device))
        self.write(json.dumps(writer_list))

class AddWriter(tornado.web.RequestHandler):
    def get(self):
        params = self.request.arguments
        writer_class = writer_types[params['writer_type'][0]]['class']
        writer_params = writer_types[params['writer_type'][0]]['defaults']
        device = params['port'][0]
        new_writer = writer_class(device, **writer_params)
        print "Adding writer", new_writer
        controller.add_writer(new_writer)

class DeviceList(tornado.web.RequestHandler):
    """
    List serial devices which are available for attaching hardware.
    """
    def get(self):
        writers = writer_types.keys()
        ports = list(list_com_ports())
        print ports
        self.write(json.dumps({'writers':writers, 'ports':ports}))

if __name__ == '__main__':
    handlers = [(r'/', Home),
                (r'/play', Play),
                (r'/autoplay_on', AutoplayOn),
                (r'/autoplay_off', AutoplayOff),
                (r'/add', AddPattern),
                (r'/pause', Pause),
                (r'/next', Next),
                (r'/pattern_groups',PatternGroups),
                (r'/status',Status)
                ]

    application = tornado.web.Application(handlers=handlers, static_path='static')
    for d in config['devices']:
        writer_class = writer_types[d['type']]['class']
        writer_params = writer_types[d['type']]['defaults']
        path = d['path']
        new_writer = writer_class(path, **writer_params)
        print "Adding writer", new_writer
        controller.add_writer(new_writer)

    controller.add_writer(LCMWriter())

    pattern_name = '_off.png'
    pattern_path = os.path.join(config['pattern_dir'], pattern_name)
    p = Bemis100Pattern(pattern_path, config['num_lights'])
    n = -1
    controller.add_pattern(p, n, name=pattern_name)

    try:
        application.listen(5000)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print 'Exiting...'
        # for c in controller.writers:
        #     c.close_port()
        controller.quit()
        print 'controller exit'
        sys.exit()
