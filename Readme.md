#Bemis 100
Firmware, software and web interface for the 1E Bemis100 lighting system.

##Dependencies
- Python 2.7
- Pillow
- numpy
- pyaudio
- tornado
- imagemagick
- rake

###Additional packages needed (on Ubuntu or similar)
- libjpeg-dev
- python2.7-dev

###Troubleshooting
If you get an error about `decoder JPEG not available`, just make sure you've installed `libjpeg-dev` and then do

	sudo pip install -I Pillow

to reinstall Pillow.

##Usage
To serve the web interface at `localhost:5000`:

	rake serve

This will take a few minutes the first time it runs to build the thumbnails, mosaics, and animated GIF previews.

