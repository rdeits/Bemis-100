from led.ledctl import LEDController
from .default_devices import DEVICES

config = {'pattern_dir': 'static/build/thumbs',
          'build_dir': 'static/build',
          'framerate': 30,
          'num_lights': 180}

devices = DEVICES

controller = LEDController(framerate=config['framerate'])
