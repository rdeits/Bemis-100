from __future__ import division

import curses
import curses.wrapper
import sys
import math


def main(stdscr):
    curses.curs_set(0)
    stdscr.addstr(0, 0, "Current mode: Typing mode",
              curses.A_REVERSE)
    stdscr.refresh()
    stdscr.addstr(1, 0, str(curses.can_change_color()))
    stdscr.addstr(2, 0, str(curses.COLOR_PAIRS))
    stdscr.addstr(3, 0, str(curses.COLORS))

    channel_max = 6
    div = 256 / channel_max
    curses.init_color(0, 0, 0, 0)

    def draw_pixel(x, r, g, b):
        r, g, b = map(int, [r / div, g / div, b / div])
        color_index = int(r * channel_max**2 + g * channel_max + b)
        pair_index = color_index + 1
        curses.init_color(color_index, r * 1000 // channel_max,
                          g * 1000 // channel_max,
                          b * 1000 // channel_max)
        curses.init_pair(pair_index, color_index, 0)
        stdscr.addch(5, x, curses.ACS_DIAMOND, curses.color_pair(pair_index))

    stdscr.addch(4, 0, curses.ACS_DIAMOND)

    draw_pixel(0, 0,0,0)
    draw_pixel(1, 255,0,0)
    draw_pixel(2, 255,255,0)
    draw_pixel(3, 255,255,255)

    stdscr.getch()
    pass

curses.wrapper(main)

