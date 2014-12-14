from __future__ import division

import led.ledctl as ledctl
import wiringpi2
import json
import sys


def encode_bits(bits):
    result = 0
    if bits[0]:
        result += 0b01000000
    else:
        result += 0b11000000

    if bits[1]:
        result += 0b00001000
    else:
        result += 0b00011000

    if bits[2]:
        result += 0b00000001
    else:
        result += 0b00000011
    return result


def bit_list(x, length):
    return [int(c) for c in ('{:0' + str(length) + 'b}').format(int(x))[:length]]

START = bytearray([0b00000001])
END = bytearray([0b00000000,0b00000000])


def encode_bulb(addr, brightness, red, green, blue):
    addr = bit_list(addr, 6)
    brightness = bit_list(brightness, 8)
    red = bit_list(red, 4)
    green = bit_list(green, 4)
    blue = bit_list(blue, 4)

    word = addr + brightness + blue + green + red + [0]
    s = str(START + bytearray([encode_bits(word[i:i+3]) for i in range(0,len(word),3)]) + END)
    # assert(len(s) == 27 + len(START) + len(END))
    return s


class GESPIWriter(ledctl.PatternWriter):
    def __init__(self, **kwargs):
        ledctl.WriterNode.__init__(self, **kwargs)
        self.open_port()

    def open_port(self):
        self.port = wiringpi2.wiringPiSPISetup(self.spi_name, 125000)
        self.blank()

    def draw_frame(self, frame):
        #print "frame"
        commands = []
        for i in range(0, len(frame), 3):
            if self.last_frame is None or any(frame[i+j] != self.last_frame[i+j] for j in range(3)):
            # if True:
                addr = i//3
                red = int(frame[i] * 15/255)
                green = int(frame[i+1] * 15/255)
                blue = int(frame[i+2] * 15/255)
                #print addr, red, blue, green
                commands.append(encode_bulb(addr, 127, red, green, blue))
                # self.write_str(encode_bulb(addr, 127, red, green, blue))
        self.write_str(''.join(commands))
        self.last_frame = frame

    def write_str(self, s):
        wiringpi2.wiringPiSPIDataRW(self.spi_name, s)


if __name__ == '__main__':
    GESPIWriter(**json.loads(sys.argv[1])).start()
