from led.ledctl import LEDController
# from led.ge import GEWriter
from led.ge_spi import GESPIWriter
from led.bemis100 import Bemis100Writer
from default_devices import DEVICES

config = {'pattern_dir': 'static/build/thumbs',
          'build_dir': 'static/build',
          'framerate': 30,
          'num_lights': 50,
          'devices': DEVICES}

controller = LEDController(framerate=config['framerate'])

writer_types = {'bemis100': {'class': Bemis100Writer,
                             'defaults': {'framerate': 30,
                                          'num_boards': 83}},
                'ge': {'class': GESPIWriter,
                       'defaults': {'framerate': 30,
                                    'num_lights': 50}}}
