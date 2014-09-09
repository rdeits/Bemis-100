from __future__ import division

import curses

import ledctl


class CursesWriter(object):
    def __init__(self, screen, num_lights, framerate=30):
        # super(CursesWriter, self).__init__(framerate)
        self.num_lights = num_lights
        self.channel_max = 6
        self.div = 256 / self.channel_max
        self.screen = screen
        self.frame_dt = 1.0 / framerate
        curses.curs_set(0)
        curses.init_color(0, 0, 0, 0)

    def open_port(self):
        pass

    def close_port(self):
        pass

    def setup(self, a, b):
        pass

    def is_alive(self):
        return True

    def send_frame(self, *args):
        pass

    def draw_pixel(self, x, r, g, b):
        r, g, b = map(int, [r / self.div, g / self.div, b / self.div])
        # x = min(x, 90)
        color_index = int(r * self.channel_max**2 + g * self.channel_max + b)
        pair_index = color_index + 1
        curses.init_color(color_index, r * 1000 // self.channel_max,
                          g * 1000 // self.channel_max,
                          b * 1000 // self.channel_max)
        curses.init_pair(pair_index, color_index, 0)
        self.screen.addch(0, x, curses.ACS_DIAMOND,
                          curses.color_pair(pair_index))

    def draw_frame(self, frame):
        for i in range(0, len(frame), 3):
            r, g, b = frame[i:i+3]
            x = i // 3
            self.draw_pixel(x, r, g, b)
        self.screen.refresh()

    def blank(self):
        self.draw_frame([0] * self.num_lights * 3)

    def start(self):
        pass



