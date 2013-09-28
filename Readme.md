#Bemis 100
Firmware, software and web interface for the 1E Bemis100 lighting system.

##Dependencies
apt-get packages shown in brackets

- Python 2.7 [python2.7]
- numpy [python-numpy]
- pyaudio [python-pyaudio]
- tornado [python-tornado]
- imagemagick [imagemagick]
- rake [rake]

You'll also need these python modules, which can be installed with Pip:

- Pillow
- pyserial


###Additional packages needed (on Ubuntu or similar)
- libjpeg-dev
- python2.7-dev

###Troubleshooting
If you get an error about `decoder JPEG not available`, just make sure you've installed `libjpeg-dev` and then do

	sudo pip install -I Pillow

to reinstall Pillow.

##Usage

Copy `Web/default_devices.example.py` to `Web/default_devices.py` and replace the `'/dev/tty.usbmodemfa131'` with the name of your device's serial port. 

To serve the web interface at `localhost:5000`:

	rake serve

This will take a few minutes the first time it runs to build the thumbnails, mosaics, and animated GIF previews.

