set -ex

passwd

sudo apt update
sudo apt install -y \
	python3-numpy \
	python3-zmq \
	python3-tornado \
	python3-pil \
	python3-pip \
	imagemagick \
	git \
	rake \
	libjpeg-dev \
	tmux \
	vim
sudo python3 -m pip install adafruit-circuitpython-dotstar

git clone https://github.com/rdeits/Bemis-100.git /home/pi/Bemis-100
cd /home/pi/Bemis-100

sudo python3 -m pip install supervisor

crontab -l | awk '{print} END {print "@reboot /usr/local/bin/supervisord -c /home/pi/Bemis-100/Web/supervisord.conf"}' | crontab
crontab -l | awk '{print} END {print "* * * * * /home/pi/Bemis-100/Web/generate_patterns.sh > /tmp/generate_patterns.log 2>&1"}' | crontab

echo "export PYTHONPATH=/home/pi/Bemis-100" >> /home/pi/.bashrc
source /home/pi/.bashrc

sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 5000

sudo apt install -y \
	iptables-persistent
