from __future__ import division

import ledctl
import serial
import time


class WS2812BWriter(ledctl.PatternWriter):

    def __init__(self, device, num_lights=150, framerate=30):
        super(WS2812BWriter, self).__init__(framerate)

        self.device = device
        self.port = None
        self.num_lights = num_lights

    def open_port(self):
        self.port = serial.Serial(port=self.device,
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

    def close_port(self):
        self.blank()
        self.port.close()
        print "Port closed"

    def draw_frame(self, frame):
        # assert(len(frame) == 3 * self.num_lights)
        # self.port.write(bytearray([x // 2 for x in frame]))
        # self.port.write(bytearray([127, 127, 0, 127, 127, 0, 0xff]))
        self.port.write(bytearray([x // 2 for x in frame] + ['\xff']))

    def blank(self):
        return
        '''Turn off all the LEDs. We do this before startup to make sure the
        power supplies are not loaded by the LEDs when they come online.'''
        print self.num_lights
        f = bytearray(reduce(str.__add__, [chr(i) + '\x00\x00\x00' for i in range(self.num_lights)]))
        print repr(f)
        self.draw_frame(f)

