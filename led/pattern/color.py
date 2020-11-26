from __future__ import division

import numpy as np
from . import pattern
from PIL import ImageColor


class SolidColor:
    def __init__(self, hex, num_lights=150):
        self.num_lights = num_lights
        self.hex = hex
        self.rgb = ImageColor.getrgb(hex)
        self.frame = np.zeros((self.num_lights, 3), dtype=np.uint8)
        for pixel in self.frame:
            pixel[0] = self.rgb[0]
            pixel[1] = self.rgb[1]
            pixel[2] = self.rgb[2]

    def start(self):
        return self

    def get_frame(self, dt):
        return self.frame
