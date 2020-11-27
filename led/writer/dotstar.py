from __future__ import division

import led.ledctl as ledctl
import sys
import json
import board
import adafruit_dotstar as dotstar


class DotstarWriter(ledctl.WriterNode):

    def __init__(self, **kwargs):
        ledctl.WriterNode.__init__(self, **kwargs)
        self.strip = dotstar.DotStar(board.SCK, board.MOSI,
            self.num_lights,
            brightness=0.2,
            auto_write=False)
        # self.strip = Adafruit_DotStar(self.num_lights)  # Use SPI (pins 10=MOSI, 11=SCLK)
        # self.strip.begin()           # Initialize pins for output
        # self.strip.setBrightness(128)
        self.blank()

    def draw_frame(self, frame):
        for (i, pixel) in enumerate(frame):
            self.strip[i] = (pixel[0], pixel[1], pixel[2])
            # self.strip.setPixelColor(i, pixel[1], pixel[0], pixel[2])
        self.strip.show()

if __name__ == '__main__':
    DotstarWriter(**json.loads(sys.argv[1])).start()
