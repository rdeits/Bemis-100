# Samba

	sudo apt-get install samba samba-common-bin
	sudo vim /etc/samba/samba.conf


In the [global] section:

	guest account=pi
	workgroup = WORKGROUP
	wins support = yes

And at the bottom:

	[Lights]
	comment=Lights patterns
	path=/home/pi/Projects/Bemis-100/Web/static/patterns
	browseable=Yes
	read only=no
	only guest=yes
	guest ok=yes
	create mask=0777
	directory mask=0777
	public=Yes

Also had do `sudo chmod -R a+x Web/static/patterns`. 

And I created `sudo vim /etc/samba/smbusers` and added:

	pi="pi"

# Cron

Need to run the `rake` target to generate the patterns and previews periodically. 

	@reboot /usr/local/bin/supervisord -c /home/pi/Projects/Bemis-100/Web/supervisord.conf
	* * * * * /home/pi/Projects/Bemis-100/Web/generate_patterns.sh > /home/pi/Projects/Bemis-100/Web/logs/generate_patterns.log 2>&1
