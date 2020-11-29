from __future__ import division

import led.ledctl as ledctl
import sys
import json
import board  # provided by adafruit-circuitpython-dotstar
import busio
import numpy as np


class DotstarWriter(ledctl.WriterNode):

    def __init__(self, **kwargs):
        ledctl.WriterNode.__init__(self, **kwargs)
        self.spi = busio.SPI(board.SCK, MOSI=board.MOSI)
        while not self.spi.try_lock():
            pass
        self.spi.configure(baudrate=4000000)
        self.blank()

    def draw_frame(self, frame):
        header = bytearray(b'\x00') * 4
        trailer_size = self.num_lights // 16
        if self.num_lights % 16 != 0:
            trailer_size += 1
        trailer = bytearray(b'\xff') * trailer_size

        permutation = (2, 1, 0)
        data = np.hstack((np.full((self.num_lights, 1), 255, dtype=np.uint8),
                          frame[:, permutation].astype(np.uint8))).tobytes()
        self.spi.write(header + data + trailer)

if __name__ == '__main__':
    DotstarWriter(**json.loads(sys.argv[1])).start()
