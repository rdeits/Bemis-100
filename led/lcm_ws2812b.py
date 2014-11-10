from __future__ import division

import ledctl
import serial
import time
import sys
import json


class WS2812BWriter(ledctl.WriterNode):

    def __init__(self, path='/dev/ttyACM0', **kwargs):
        ledctl.WriterNode.__init__(self, **kwargs)
        self.path = path
        self.open_port()

    def open_port(self):
        self.port = serial.Serial(port=self.path,
                # baudrate=9600,
                baudrate=230400,
                bytesize=serial.EIGHTBITS,
                stopbits=serial.STOPBITS_ONE,
                parity=serial.PARITY_NONE,
                timeout=2,
                writeTimeout=0)
        time.sleep(3)
        # self.bytes_since_ack = 0
        self.blank()

    def draw_frame(self, frame):
        # assert(len(frame) == 3 * self.num_lights)
        # self.port.write(bytearray([x // 2 for x in frame]))
        # self.port.write(bytearray([127, 127, 0, 127, 127, 0, 0xff]))
        self.port.write(bytearray([x // 2 for x in frame] + ['\xff']))


if __name__ == '__main__':
    WS2812BWriter(**json.loads(sys.argv[1])).start()
