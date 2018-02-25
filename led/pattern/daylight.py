import time
import datetime
import numpy as np


class DaylightPattern:
    def __init__(self,
                 num_lights,
                 sunrise=datetime.time(hour=5),
                 sunset=datetime.time(hour=23, minute=0),
                 transition=datetime.timedelta(minutes=1)):
        self.num_lights = num_lights
        self.sunrise = sunrise
        self.sunset = sunset
        self.transition = transition
        self.frame = np.zeros((num_lights, 3))
        self.last_frame_time = None

    def __iter__(self):
        return self

    def next(self):
        now = datetime.datetime.now().time()
        if self.sunrise < self.sunset:
            # sunrise and sunset on same day, e.g.
            # sunrise at 0600, sunset at 1800
            daylight = self.sunrise < now < self.sunset
        else:
            # sunset happens on the subsequent day, e.g.
            # sunrise at 0600, sunset at 0100 the next day
            daylight = now > self.sunrise or now < self.sunset

        if daylight:
            self.frame.fill(255)
        else:
            self.frame.fill(0)
        return self.frame.astype(np.uint8)



