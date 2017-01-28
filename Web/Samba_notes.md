
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
