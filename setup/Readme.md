# Setting up the Raspberry Pi

1. Flash Raspbian to the micro SD card using Etcher
2. Create a file called `ssh` in the `boot` partition
3. Create a `wpa_supplicant.conf` in the `boot` partition with:

    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country=US

    network={
        ssid="«your_SSID»"
        psk="«your_PSK»"
        key_mgmt=WPA-PSK
    }


4. Log into the pi and run the `setup_pi.sh` script

5. Enable SPI by editing /boot/config.txt and uncommenting `dtparam=spi=on` or by changing the setting in `sudo raspi-config`
