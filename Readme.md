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
- libjpeg-dev
- python2.7-dev
- python-zmq

You'll also need these python modules, which can be installed with Pip:

- Pillow
- pyserial


###Troubleshooting
If you get an error about `decoder JPEG not available`, just make sure you've installed `libjpeg-dev` and then do

	sudo pip install -I Pillow

to reinstall Pillow.

##Usage

Copy `Web/default_devices.example.py` to `Web/default_devices.py` and replace the `'/dev/tty.usbmodemfa131'` with the name of your device's serial port.

To serve the web interface at `localhost:5000`:

	rake serve

This will take a few minutes the first time it runs to build the thumbnails, mosaics, and animated GIF previews.


## Supervisord

supervisord is used on boot to run the `rake serve` task.

Install it by doing:

	sudo pip install supervisor
	sudo pip install -U distribute

To edit the supervisord configuration file, kill all processes with supervisord, edit the configuration file, and either reboot or restart supervisord with

`/usr/local/bin/supervisord -c /home/pi/Projects/Bemis-100/Web/supervisord.conf`

To get it to run on boot, do `crontab -e` and add the following line:

`@reboot /usr/local/bin/supervisord -c /home/pi/Projects/Bemis-100/Web/supervisord.conf`

You need the `/usr/local/bin` prefix in there to make sure you don't need to run as root.

The supervisord configuration currently assumes a hard-coded path to the project at `/home/pi/Projects/Bemis-100`.

## Avahi Configuration

Some versions of raspbian appear to advertise an avahi service, but others do not. To be safe, we'll create our own service definition. To do so, create `/etc/avahi/services/lights.service` and set its contents to:

```xml
<?xml version="1.0" standalone='no'?><!--*-nxml-*-->
<!DOCTYPE service-group SYSTEM "avahi-service.dtd">

<service-group>

  <name replace-wildcards="yes">%h</name>

  <service>
    <type>_http._tcp</type>
    <port>80</port>
  </service>

</service-group>
