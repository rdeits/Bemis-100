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

        # Construct an SPI interface to control the dotstar LEDs directly. The
        # `adafruit_dotstar` package also works, but its interface is extremely
        # slow and cannot keep up with real-time drawing of the LED strip.
        self.spi = busio.SPI(board.SCK, MOSI=board.MOSI)
        while not self.spi.try_lock():
            pass
        self.spi.configure(baudrate=4000000)

        self._pwm_bytes = np.full((self.num_lights, 1), 255, dtype=np.uint8)
        self._header = bytearray(b'\x00') * 4
        trailer_size = self.num_lights // 16
        if self.num_lights % 16 != 0:
            trailer_size += 1
        self._trailer = bytearray(b'\xff') * trailer_size

        self.blank()

    def draw_frame(self, frame):
        permutation = (2, 1, 0)
        permuted = frame.astype(np.uint8)[:, permutation]
        scaled = np.right_shift(permuted, 2)
        data = np.hstack((self._pwm_bytes, scaled)).tobytes()
        self.spi.write(self._header + data + self._trailer)

if __name__ == '__main__':
    DotstarWriter(**json.loads(sys.argv[1])).start()
