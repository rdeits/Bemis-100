from __future__ import division

import led.ledctl as ledctl
import sys
import json
import board
import busio


class DotstarWriter(ledctl.WriterNode):

    def __init__(self, **kwargs):
        ledctl.WriterNode.__init__(self, **kwargs)
        self.spi = busio.SPI(board.SCK, MOSI=board.MOSI)
        while not self.spi.try_lock():
            pass
        spi.configure(baudrate=4000000)

        # self.strip = dotstar.DotStar(board.SCK, board.MOSI,
        #     self.num_lights,
        #     brightness=0.2,
        #     auto_write=False)
        # self.strip = Adafruit_DotStar(self.num_lights)  # Use SPI (pins 10=MOSI, 11=SCLK)
        # self.strip.begin()           # Initialize pins for output
        # self.strip.setBrightness(128)
        self.blank()

    def draw_frame(self, frame):
        header = bytearray(b'\x00') * 4
        trailer_size = self.num_lights // 16
        if self.num_lights % 16 != 0:
            trailer_size += 1
        trailer = bytearray(b'\xff') * trailer_size

        permutation = (2, 1, 0)
        data = np.hstack(np.full((self.num_lights, 1), 255, dtype=np.uint8),
                         frame[:, p].astype(np.uint8)).tobytes()
        # for (i, pixel) in enumerate(frame):
        #     self.strip[i] = (pixel[0], pixel[1], pixel[2])
        #     # self.strip.setPixelColor(i, pixel[1], pixel[0], pixel[2])
        # self.strip.show()
        self.spi.write(header + data + trailer)

if __name__ == '__main__':
    DotstarWriter(**json.loads(sys.argv[1])).start()
