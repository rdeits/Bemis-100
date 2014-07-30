from __future__ import division

import wiringpi2
import ledctl
import os


def encode_bit(bit):
    if bit:
        return 0b11111000
    else:
        return 0b11100000


def bit_list(x, length=8):
    return [int(c) for c in ('{:0' + str(length) + 'b}').format(int(x))[:length]]

END = bytearray([0b00000000]*100)


class WS2812BWriter(ledctl.PatternWriter):

    def __init__(self, device, num_lights=150, framerate=30):
        super(WS2812BWriter, self).__init__(framerate)

        self.device = device
        self.port = None
        self.spi_name = 1
        self.num_lights = num_lights

    def open_port(self):
        self.port = wiringpi2.wiringPiSPISetup(self.spi_name, 8000000)
        self.blank()

    def close_port(self):
        self.blank()

    def draw_frame(self, frame):
        #print "frame"
        print len(frame)
        commands = bytearray([])
        for i in range(0, len(frame), 3):
            red = frame[i] // 2
            green = frame[i+1] // 2
            blue = frame[i+2] // 2
            bits = bit_list(green) + bit_list(red) + bit_list(blue)
            commands.extend(bytearray([encode_bit(x) for x in bits]))
        commands.extend(END)
        print len(commands)
        self.write_str(str(commands))

    def write_str(self, s):
        # os.write(self.port, s)
        wiringpi2.wiringPiSPIDataRW(self.spi_name, s)

    def blank(self):
        self.draw_frame([25,0,0]*self.num_lights)


