from __future__ import division

# import multiprocessing
import threading
import numpy as np
import time
from collections import namedtuple
from itertools import count
import zmq

QueueItem = namedtuple('QueueItem', ['name', 'pattern', 'reps', 'id'])

IDCounter = count()

class LEDController(object):
    def __init__(self, framerate=30, port=5555):
        self.frame_dt = 1.0 / framerate

        self.current = None

        self._play = threading.Event()    # Continue playing; if not set, enter pause mode,
                                                # staying on the same pattern

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.port = port
        self.socket.bind("tcp://*:{:d}".format(self.port))
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
        metadata = {'dtype': str(frame.dtype),
              'shape': frame.shape}
        self.socket.send_json(metadata, zmq.SNDMORE)
        self.socket.send(frame, flags=0,
                         copy=True, track=False)


class WriterNode(object):
    def __init__(self, host="localhost", port=5555, num_lights=150):
        self.port = port
        self.host = host
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, u"")
        self.socket.connect("tcp://{:s}:{:d}".format(self.host, int(self.port)))
        self.num_lights = num_lights

    def draw_frame(self, frame):
        raise NotImplementedError

    def start(self):
        while True:
            metadata = self.socket.recv_json(flags=0)
            message = self.socket.recv(flags=0, copy=True, track=False)
            buf = buffer(message)
            frame = np.frombuffer(buf, dtype=metadata['dtype']).reshape(metadata['shape'])
            self.draw_frame(frame)

    def stop(self):
        pass

    def blank(self):
        f = np.zeros((self.num_lights, 3), dtype=np.int)
        self.draw_frame(f)


