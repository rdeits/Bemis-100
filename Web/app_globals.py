from led.ledctl import LEDController
from default_devices import DEVICES

config = {'pattern_dir': 'static/build/thumbs',
          'build_dir': 'static/build',
          'framerate': 20,
          'num_lights': 150}

devices = DEVICES

controller = LEDController(framerate=config['framerate'])
