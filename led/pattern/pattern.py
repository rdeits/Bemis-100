#!/usr/bin/env python2.6
from __future__ import division

import PIL.Image as im
import numpy as np

'''This program generates patterns for the Bemis100 lighting system. A pattern
is derived from an image file, which will be played back one row at a time on
the Bemis100.
'''

class PatternState:
    def __init__(self, image_data, rows_per_second=30):
        self.image_data = image_data
        self.rows_per_second = rows_per_second
        self.t = 0
        self.frame = image_data[0].copy().astype(np.float64)

    def get_frame(self, dt):
        self.t += dt
        row_position = self.t * self.rows_per_second
        previous_row = int(row_position)
        next_row = previous_row + 1
        alpha = row_position - previous_row

        if next_row >= len(self.image_data):
            return None

        if alpha <= 0:
            return self.image_data[previous_row]
        if alpha >= 1:
            return self.image_data[next_row]

        self.frame *= 0
        self.frame += self.image_data[previous_row]
        self.frame *= (1 - alpha) / alpha
        self.frame += self.image_data[next_row]
        self.frame *= alpha
        return self.frame.astype(np.uint8)


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
        self.image_data = np.array(image, dtype=np.uint8)

    def start(self):
        return PatternState(self.image_data)


    # def __iter__(self):
    #     return iter(self.image_data)


