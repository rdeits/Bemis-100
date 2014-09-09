#!/usr/bin/env python2.6
from __future__ import division

import PIL.Image as im
import numpy as np

'''This program generates patterns for the Bemis100 lighting system. A pattern
is derived from an image file, which will be played back one row at a time on
the Bemis100.
'''

class Bemis100Pattern:
    def __init__(self, filename, num_lights=0):
        self.filename = filename
        self.current_row = 0
        self.read_image(num_lights)

    def read_image(self, target_width=0):
        '''Read the image, then create an array with the data in the correct
        format for the Bemis100.'''
        image = im.open(self.filename)
        (width,height)=image.size

        if target_width == 0:
            target_width = width
        target_height = 2 * height
        image = image.resize((int(target_width), target_height), im.ANTIALIAS)
        (width, height) = image.size

        image = image.convert('RGB')
        arr = np.array(image, dtype=np.uint8)
        self.image_data = [bytearray(x) for x in arr.reshape((height, width*3))]
        # self.image_data = arr.reshape((height, width*3))


    def __iter__(self):
        return iter(self.image_data)


