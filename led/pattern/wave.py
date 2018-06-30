from __future__ import division

from multiprocessing import Process, Pipe
import itertools
import random

import numpy as np

import pattern

T = .5; # "Tension"
mu = 1; # "mass per length"
friction = 0.01; # frictional force per velocity
# dt = .5;

class WavePattern:
    def __init__(self,num_lights = 166):
        self.pixels = num_lights
        print self.pixels, "pixels in use"
        self.pos = np.zeros(self.pixels)
        self.vel = np.zeros(self.pixels)
        self.acc = np.zeros(self.pixels)
        self.out = np.zeros((self.pixels, 3))

    def get_line(self):
        self.update_physics()

        if random.random() < .01:
            self.add_pulse()

        for i in range(self.pixels):
            self.out[i] = self.output_func(self.pos[i])

        return self.out

    def update_physics(self, dt):
        self.acc[1:self.pixels-1] = ((self.pos[2:self.pixels]-\
                2*self.pos[1:self.pixels-1]+\
                self.pos[0:self.pixels-2])*T-friction*self.vel[1:self.pixels-1])/mu

        self.vel[1:self.pixels-1] += self.acc[1:self.pixels-1]*dt*15

        # self.vel[1:self.pixels-1] *= .95

        self.pos[1:self.pixels-1] += self.vel[1:self.pixels-1]*dt*15

    def output_func(self, point):
        if point > 1:
            point = 1
        elif point < -1:
            point = -1
        if point > 0:
            out = [0, 0, int(point*255)]
        elif point < 0:
            out = [int(-point*255), 0, 0]
        else:
            out = [0, 0, 0]
        return out


    def add_pulse(self):
        pulse_center = random.randrange(0, self.pixels)
        pulse_width = random.randrange(1, 15)
        if random.random() < .5:
            pulse_sign = -1
        else:
            pulse_sign = 1
        self.pos[max(1, pulse_center - pulse_width//2):min(self.pixels-1,
                                                           pulse_center + pulse_width//2)] = pulse_sign

    def start(self):
        pulse_width = 20
        start_data = np.array(\
                [0]+\
                [0]*int(np.floor(self.pixels/2-(pulse_width//2+1)))+\
                [1]*pulse_width+\
                [0]*int(np.ceil(self.pixels/2-(pulse_width//2+1)))+\
                [0])
        print "start data", start_data
        # start_data = np.array(\
                # [0]+\
                # [1]*20+\
                # [0]*int(self.pixels-22)+\
                # [0])

        self.pos += start_data
        return self

    def get_frame(self, dt):
        self.update_physics(dt)



    # def __iter__(self):
    #     pulse_width = 20
    #     start_data = np.array(\
    #             [0]+\
    #             [0]*int(np.floor(self.pixels/2-(pulse_width//2+1)))+\
    #             [1]*pulse_width+\
    #             [0]*int(np.ceil(self.pixels/2-(pulse_width//2+1)))+\
    #             [0])
    #     print "start data", start_data
    #     # start_data = np.array(\
    #             # [0]+\
    #             # [1]*20+\
    #             # [0]*int(self.pixels-22)+\
    #             # [0])

    #     self.pos += start_data
    #     return (self.get_line() for i in itertools.repeat(True))
    #     # return iter(self.get_line,None)



