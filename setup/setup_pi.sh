set -ex

passwd

sudo apt update
sudo apt install -y \
	python-numpy \
	python-zmq \
	python-tornado \
	python-pil \
	python-pip \
	imagemagick \
	git \
	rake \
	libjpeg-dev \
	tmux \
	vim \

git clone https://github.com/rdeits/Bemis-100.git /home/pi/Bemis-100
cd /home/pi/Bemis-100

sudo pip install supervisor

crontab -l | awk '{print} END {print "@reboot /usr/local/bin/supervisord -c /home/pi/Bemis-100/Web/supervisord.conf"}' | crontab
crontab -l | awk '{print} END {print "* * * * * /home/pi/Bemis-100/Web/generate_patterns.sh > /tmp/generate_patterns.log 2>&1"}' | crontab

echo "export PYTHONPATH=/home/pi/Bemis-100" >> /home/pi/.bashrc
source /home/pi/.bashrc