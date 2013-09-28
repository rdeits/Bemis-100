import sys
import random
import time
import os
import numpy as np

sys.path.append('..')
from led.pattern import Bemis100Pattern
from led.utils import find_patterns_flat

class MixPattern:
    def __init__(self, folder, num_lights=50):
        self.folder = os.path.split(folder)[0]
        self.num_lights = num_lights
        self.pattern_paths = find_patterns_flat(self.folder)
        self.patterns = []
        self.build_patterns()

    def build_patterns(self):
        for p in self.pattern_paths:
            pat = Bemis100Pattern(p, self.num_lights)
            self.patterns.append(pat)

    def __iter__(self):
        return MixPattern.shuffle(*self.patterns)

    @staticmethod
    def shuffle(*iters):
        last_frame = None
        fade = 1
        while True:
            p = iters[random.randrange(0, len(iters))]
            n = random.randrange(1,3)
            start_time = time.time()
            timed_out = False
            fade = 1
            for j in range(n):
                for x in p:
                    fade = max(fade - 0.05, 0)
                    if fade > 0 and last_frame is not None:
                        out = bytearray(int(round(c)) for c in np.array(x) * (1-fade) + np.array(last_frame) * fade)
                        # print map(int, x), map(int, out)
                    else:
                        out = x
                    yield out
                    if time.time() - start_time > 120:
                        timed_out = True
                        break
                last_frame = x
                if timed_out:
                    break
