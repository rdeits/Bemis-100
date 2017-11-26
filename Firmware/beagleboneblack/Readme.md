# BeagleBone Black Wireless Setup

Installed Debian 9.2 IoT edition <https://debian.beagleboard.org/images/bone-debian-9.2-iot-armhf-2017-10-10-4gb.img.xz> from <https://beagleboard.org/latest-images> to a 4 Gb Micro SD card. 

Booted the BBB over USB and was able to log in with:

	ssh debian@beaglebone.local

using the default password `temppwd`. Changed it.

### Setting up WiFi

There appears to be no wifi at all from my device at initial setup. The BBBW docs claim that it will create a BeagleBone-XXXX network, but it does not, and there's no wlan network interface. This forum post: <https://groups.google.com/forum/?fromgroups#!searchin/beagleboard/connmanctl|sort:date/beagleboard/a1V_8dLoGXs/lLHiEJcoAAAJ> suggests that the eeprom is mis-programmed. 

To try to get it working, I soldered header onto TP1 (a hole labeled in the silkscreen) and then connected that to ground (pin 1 or 2), and then ran:

	sudo dd if=/opt/scripts/device/bone/bbbw-eeprom.dump of=/sys/devices/platform/ocp/44e0b000.i2c/i2c-0/0-0050/eeprom
	sudo reboot

This caused the `wlan0` interface to show up in `ifconfig`, and caused the BeagleBone to start broadcasting its wireless network. Before running the above, I had:

```
debian@beaglebone:~$ sudo /opt/scripts/tools/version.sh
[sudo] password for debian:
git:/opt/scripts/:[d36fe9a7be9ebfc872b10a470e904ab4c61c4516]
eeprom:[A335BNLT0371*]
dogtag:[BeagleBoard.org Debian Image 2017-10-10]
bootloader:[microSD-(push-button)]:[/dev/mmcblk0]:[U-Boot 2017.09-00002-g0f3f1c7907]
bootloader:[eMMC-(default)]:[/dev/mmcblk1]:[U-Boot 2017.01-00006-g55e748eda0]
kernel:[4.4.91-ti-r133]
nodejs:[v6.11.4]
uboot_overlay_options:[enable_uboot_overlays=1]
uboot_overlay_options:[uboot_overlay_pru=/lib/firmware/AM335X-PRU-RPROC-4-4-TI-00A0.dtbo]
uboot_overlay_options:[enable_uboot_cape_universal=1]
pkg:[bb-cape-overlays]:[4.4.20171009.0-0rcnee1~stretch+20171009]
pkg:[bb-wl18xx-firmware]:[1.20170829-0rcnee1~stretch+20170829]
pkg:[firmware-ti-connectivity]:[20170823-1rcnee0~stretch+20170830]
```

and after, I had:

```
debian@beaglebone:~$ sudo /opt/scripts/tools/version.sh
[sudo] password for debian:
git:/opt/scripts/:[d36fe9a7be9ebfc872b10a470e904ab4c61c4516]
eeprom:[A335BNLTBWA50000BBWG*]
dogtag:[BeagleBoard.org Debian Image 2017-10-10]
bootloader:[microSD-(push-button)]:[/dev/mmcblk0]:[U-Boot 2017.09-00002-g0f3f1c7907]
bootloader:[eMMC-(default)]:[/dev/mmcblk1]:[U-Boot 2017.01-00006-g55e748eda0]
kernel:[4.4.91-ti-r133]
nodejs:[v6.11.4]
uboot_overlay_options:[enable_uboot_overlays=1]
uboot_overlay_options:[uboot_overlay_pru=/lib/firmware/AM335X-PRU-RPROC-4-4-TI-00A0.dtbo]
uboot_overlay_options:[enable_uboot_cape_universal=1]
pkg:[bb-cape-overlays]:[4.4.20171009.0-0rcnee1~stretch+20171009]
pkg:[bb-wl18xx-firmware]:[1.20170829-0rcnee1~stretch+20170829]
pkg:[firmware-ti-connectivity]:[20170823-1rcnee0~stretch+20170830]
```

(note the change in `eeprom` output). 

This also magically fixed `connmanctl`. To connect to wifi, I followed <https://www.digikey.com/en/maker/blogs/how-to-setup-wifi-on-the-beaglebone-black-wireless/f6452fa17bd24347a59f306355ebfef8> and did:

	sudo connmanctl
	enable wifi
	scan wifi
	services
	agent on
	connect wifi_xxxxxx_xxxxxxx (matching the output from `services`)
	(entered the passphrase)
	quit

after which I finally had wifi access. 

## Basic PRU Usage

Following instructions from <https://gist.github.com/jadonk/2ecf864e1b3f250bad82c0eae12b7b64>:

	git clone https://gist.github.com/jadonk/2ecf864e1b3f250bad82c0eae12b7b64
	cd 2ecf864e1b3f250bad82c0eae12b7b64
	make
	echo none > /sys/class/leds/beaglebone\:green\:usr0/trigger

(at this point, the USR0 LED stops blinking)

	sudo config-pin overlay cape-universala
	sudo config-pin p9.30 pruout

the last line threw an error:

	P9_30 pinmux file not found!
	bash: /sys/devices/platform/ocp/ocp*P9_30_pinmux/state: No such file or directory
	Cannot write pinmux file: /sys/devices/platform/ocp/ocp*P9_30_pinmux/state

but seemed to work anyway? To run the code, I did:

	sudo make run

and the USR0 LED started blinking!

https://elinux.org/EBC_Exercise_30_PRU_via_remoteproc_and_RPMsg
http://processors.wiki.ti.com/index.php/PRU_Projects

# Existing LED WS2812 implementation:

https://trmm.net/Category:LEDscape
https://github.com/osresearch/LEDscape

