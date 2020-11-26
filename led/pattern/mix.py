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
            print("created", pat)
            self.patterns.append(pat)

    def __iter__(self):
        return MixPattern.shuffle(*self.patterns)

    @staticmethod
    def shuffle(*iters):
        last_frame = None
        fade = 1
        while True:
            pattern = random.sample(iters, 1)[0]
            num_repeats = random.randrange(1,3)
            start_time = time.time()
            timed_out = False
            fade = 1
            for j in range(num_repeats):
                for frame in pattern:
                    fade = max(fade - 0.05, 0)
                    if fade > 0 and last_frame is not None:
                        out = (1 - fade) * frame + fade * last_frame
                    else:
                        out = frame
                    yield out.astype(np.uint8)
                    if time.time() - start_time > 120:
                        timed_out = True
                        break
                last_frame = frame
                if timed_out:
                    break
