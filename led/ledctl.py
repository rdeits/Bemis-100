from __future__ import division

# import multiprocessing
import threading
import numpy as np
import time
from collections import namedtuple
from itertools import count
import lcm
import bemis100LCM

QueueItem = namedtuple('QueueItem', ['name', 'pattern', 'reps', 'id'])

IDCounter = count()

class LEDController(object):
    def __init__(self, framerate=30):
        self.frame_dt = 1.0 / framerate

        self.current = None

        self._play = threading.Event()    # Continue playing; if not set, enter pause mode,
                                                # staying on the same pattern

        self.lc = lcm.LCM('udpm://239.255.76.67:7667?ttl=1')
        self.new_pattern = threading.Event()
        self.run_thread = threading.Thread(target=self.run)
        self.run_thread.daemon = True
        self.run_thread.start()

    def add_pattern(self, pattern, num_times=-1, name=''):
        if pattern is None:
            self.current = None
        else:
            self.current = QueueItem(name, pattern, num_times, IDCounter.next())
            self.new_pattern.set()

        self.play()

    def play(self):
        self._play.set()

    def pause(self):
        self._play.clear()

    def is_playing(self):
        return self._play.is_set()

    def wait_for_data(self):
        while self.current is None:
            self.new_pattern.wait(0.1)

    def quit(self):
        self.add_pattern(None)

    def run(self):
        while True:
            self.wait_for_data()

            if self.current is not None:
                self.draw_pattern(self.current.pattern, self.current.reps)
            else:
                print "Controller exiting..."

    def draw_pattern(self, pattern, num_times):
        count = 0
        while True:
            if (num_times > 0 and count == num_times):
                break

            row_start = time.time()
            if pattern is None:
                self.exit()

            for frame in pattern:
                if not self._play.is_set():
                    self._play.wait()

                if self.new_pattern.is_set():
                    self.new_pattern.clear()
                    return

                self.draw_frame(frame)

                dt = time.time() - row_start
                if dt < self.frame_dt:
                    time.sleep(self.frame_dt - dt)
                # else:
                #     print 'Draw slow by %f sec' % (dt-self.frame_dt)

                row_start = time.time()

            count += 1

    def draw_frame(self, frame):
        msg = bemis100LCM.frame_t()
        msg.n_pixels = len(frame) // 3
        frame = np.asarray(frame)
        msg.red = frame[range(0, len(frame), 3)]
        msg.green = frame[range(1, len(frame), 3)]
        msg.blue = frame[range(2, len(frame), 3)]
        self.lc.publish('BEMIS_100_DRAW', msg.encode())


class WriterNode(object):
    def __init__(self,  channel='BEMIS_100_DRAW', num_lights=150):
        self.channel = channel
        self.lc = lcm.LCM()
        self.lc.subscribe(self.channel, self.handle_frame_message)
        self.num_lights = num_lights

    def handle_frame_message(self, channel, data):
        msg = bemis100LCM.frame_t.decode(data)
        frame = np.vstack((np.fromstring(msg.red, dtype=np.uint8),
                           np.fromstring(msg.green, dtype=np.uint8),
                           np.fromstring(msg.blue, dtype=np.uint8))).T
        self.draw_frame(frame)

    def draw_frame(self, frame):
        raise NotImplementedError

    def start(self):
        while True:
            self.lc.handle()

    def stop(self):
        pass

    def blank(self):
        f = np.zeros((self.num_lights, 3), dtype=np.int)
        # f = bytearray(reduce(str.__add__, [chr(i) + '\x00\x00\x00' for i in range(self.num_lights)]))
        self.draw_frame(f)


