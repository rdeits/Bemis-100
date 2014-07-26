from __future__ import division

import wiringpi2
import ledctl


def encode_bit(bit):
    if bit:
        return 0b00001111
    else:
        return 0b00111111


def bit_list(x, length):
    return [int(c) for c in ('{:0' + str(length) + 'b}').format(int(x))[:length]]

START = bytearray([0b00000111])
END = bytearray([0b00000000, 0b00000000])


def encode_bulb(addr, brightness, red, green, blue):
    addr = bit_list(addr, 6)
    brightness = bit_list(brightness, 8)
    red = bit_list(red, 4)
    green = bit_list(green, 4)
    blue = bit_list(blue, 4)

    s = str(START + bytearray([encode_bit(x) for x in
            addr + brightness + blue + green + red]) + END)
    assert(len(s) == 26 + len(START) + len(END))
    return s


class GESPIWriter(ledctl.PatternWriter):

    def __init__(self, device, num_lights=50, framerate=30):
        super(GESPIWriter, self).__init__(framerate)

        self.device = device
        self.port = None
        self.num_lights = num_lights
        self.last_frame = None

    def open_port(self):
        self.port = 1
        wiringpi2.wiringPiSPISetup(self.port, 250000)
        self.blank()

    def close_port(self):
        self.blank()

    def draw_frame(self, frame):
        
        for i in range(0, len(frame), 3):
            if self.last_frame is None or any(frame[i+j] != self.last_frame[i+j] for j in range(3)):
                addr = i//3
                red = int(frame[i] * 15/255)
                green = int(frame[i+1] * 15/255)
                blue = int(frame[i+2] * 15/255)
                #print addr, red, blue, green
                self.write_str(encode_bulb(addr, 127, red, green, blue))
        self.last_frame = frame

    def write_str(self, s):
        wiringpi2.wiringPiSPIDataRW(self.port, s)

    def blank(self):
        for addr in range(self.num_lights):
            self.write_str(encode_bulb(addr, 127, 15, 0, 0))

