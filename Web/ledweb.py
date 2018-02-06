import tornado.web
import tornado.ioloop
import subprocess
import os
import re
import json

import sys
from app_globals import controller, config, devices
from led.pattern import Bemis100Pattern
# from led.pattern.beat import BeatPattern
# from led.pattern.graphEq import GraphEqPattern
from led.pattern.wave import WavePattern
from led.pattern.new_wave import NewWavePattern
from led.pattern.mix import MixPattern
from led.utils import find_patterns


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

        status['playing'] = controller.is_playing()
        self.write(json.dumps({'controller_status': status}))


def handle_add_pattern(params, persist=True):
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
    if persist:
        with open("last_command.json", "w") as f:
            json.dump(params, f)


class AddPattern(tornado.web.RequestHandler):
    def get(self):
        params = self.request.arguments
        handle_add_pattern(params)
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

class Next(tornado.web.RequestHandler):
    def get(self):
        print "next"
        controller.next()
        self.write(json.dumps(dict(success=True)))

if __name__ == '__main__':
    handlers = [(r'/', Home),
                (r'/play', Play),
                (r'/add', AddPattern),
                (r'/pause', Pause),
                (r'/next', Next),
                (r'/pattern_groups',PatternGroups),
                (r'/status',Status)
                ]

    application = tornado.web.Application(handlers=handlers, static_path='static')

    procs = []
    for d in devices:
        args = {'num_lights': config['num_lights']}
        args.update(d['args'])
        serialized_args = json.dumps(args)
        print serialized_args
        procs.append(subprocess.Popen(['python', '-m', d['class'], serialized_args]))

    pattern_name = '_off.png'
    pattern_path = os.path.join(config['pattern_dir'], pattern_name)
    p = Bemis100Pattern(pattern_path, config['num_lights'])
    n = -1
    controller.add_pattern(p, n, name=pattern_name)

    if os.path.exists("last_command.json"):
        with open("last_command.json", "r") as f:
            try:
                params = json.load(f)
                handle_add_pattern(params, False)
            except:
                print "could not load previous command"
                raise

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 5000

    try:
        application.listen(port)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print 'Exiting...'
        # for c in controller.writers:
        #     c.close_port()
    except Exception as e:
        print e
        raise
    finally:
        controller.quit()
        print 'controller exit'
        for proc in procs:
            proc.kill()
        sys.exit()
