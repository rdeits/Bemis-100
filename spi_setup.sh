sudo modprobe spi_bcm2708
sudo modprobe spidev bufsiz=12
sudo chown `id -u`.`id -g` /dev/spidev0.*
