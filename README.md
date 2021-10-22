# rpi-sense-hat-uf
Raspberry Pi - Sense Hat to Splunk UF

# Installation
## Install the sense-hat libraries for RPi. 
It is probably already installed, but if not ...
```
$ sudo apt-get install sense-hat
```

## Clone this repo
```
$ git clone https://github.com/thing-a-verse/rpi-sense-hat-uf.git
```


## Start the sensor
In a terminal window, Start the sensor
```
$ cd rpi-sense-hat-uf
$ ./datalog.py
```

In another terminal windows, Check the data is being generated. If it's working you'll also see
the temperature displayed on the LED display
```
$ cd rpi-sense-hat-uf
$ tail -f data.csv
```


# Install the Splunk Universal Forwarder (UF)

## Software - How to get it
### Method 1
Go to the Splunk website
https://splunk.com/en_us/download/universal-forwarder.html

Login

Choose the installation package from the __Linux__ tab.  
Download the package for __ARM__  
e.g. [4.14+, 5.x+ kernel Linux distributions, Graviton & Graviton2 Servers 64-bit]

Accept the Software Agreement, and download the `.tgz` file

### Method 2
If you are using RPi 4 ... You can use ARMv8 code in the latest veresion 8.2.2.1 (or whatever)
```
$ wget -O splunkforwarder-8.2.2.1-ae6821b7c64b-Linux-armv8.tgz 'https://download.splunk.com/products/universalforwarder/releases/8.2.2.1/linux/splunkforwarder-8.2.2.1-ae6821b7c64b-Linux-armv8.tgz'


```
or, if you have an RPi 3 ... get the older ARMv6 code from v8.1.4
```
wget -O splunkforwarder-8.1.4-17f862b42a7c-Linux-arm.tgz 'https://download.splunk.com/products/universalforwarder/releases/8.1.4/linux/splunkforwarder-8.1.4-17f862b42a7c-Linux-arm.tgz'
```
### Method 3
Run the fetch program
```
$ ./fetchSplunkUF.py
```
# Install the UF

Try reading the fine manuals, here https://docs.splunk.com/Documentation/Forwarder/8.2.2/Forwarder/Abouttheuniversalforwarder
Specifically: https://docs.splunk.com/Documentation/Forwarder/8.2.2/Forwarder/Installanixuniversalforwarder

or

### Install it as the pi user as follows
RPi 4...
```
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo tar -xvsf splunkforwarder-8.2.2.1-ae6821b7c64b-Linux-armv8.tgz -C /opt

```
RPi 3...
```
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo tar -xvsf splunkforwarder-8.1.4-17f862b42a7c-Linux-arm.tgz -C /opt

```



Per the fine manuals, it's not best practice to run Splunk as root
https://docs.splunk.com/Documentation/Splunk/8.2.2/Installation/RunSplunkasadifferenttornon-rootuser

```
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo chown -R pi:pi /opt/splunkforwarder/

```

### Configure $SPLUNK_HOME
```
pi@raspberrypi:~/rpi-sense-hat-uf $ vi ~/.profile 
```
Add the follongline to the bottom
```
export SPLUNK_HOME=/opt/splunkforwarder
```
Don't forget to re-source the `.profile` (or close the terminal windows and re-open a new one)
```
pi@raspberrypi:~/rpi-sense-hat-uf $ . ~/.profile
pi@raspberrypi:~/rpi-sense-hat-uf $ echo $SPLUNK_HOME
/opt/splunkforwarder
pi@raspberrypi:~/rpi-sense-hat-uf $ 

```




### ChangeDir to $SPLUNK_HOME/bin
```
pi@raspberrypi:~ $ cd $SPLUNK_HOME/bin
pi@raspberrypi:/opt/splunkforwarder/bin $
```

### Now accept the EULA
```
./splunk start --accept-license
```
__NOTE__: If you get the error `bash: ./splunk: cannot execute binary file: Exec format error`, you installed the wrong version on your RPI 3  
Backtrack as follows
```
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo rm -rf /opt/splunkforwarder
pi@raspberrypi:~/rpi-sense-hat-uf $ wget -O splunkforwarder-8.1.4-17f862b42a7c-Linux-arm.tgz 'https://download.splunk.com/products/universalforwarder/releases/8.1.4/linux/splunkforwarder-8.1.4-17f862b42a7c-Linux-arm.tgz'
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo tar -xvsf splunkforwarder-8.1.4-17f862b42a7c-Linux-arm.tgz -C /opt
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo chown -R pi:pi /opt/splunkforwarder/
pi@raspberrypi:~ $ cd $SPLUNK_HOME/bin
./splunk start --accept-license
```



If successful, you'll see
```
pi@raspberrypi:/opt/splunkforwarder/bin $ ./splunk start --accept-license

This appears to be your first time running this version of Splunk.

Splunk software must create an administrator account during startup. Otherwise, you cannot log in.
Create credentials for the administrator account.
Characters do not appear on the screen when you type in credentials.

Please enter an administrator username:

``` 

Your choice, i use:
`admin`  
`passw0rd`  
o

Spplunk should start
```
pi@raspberrypi:/opt/splunkforwarder/bin $ ./splunk start --accept-license

This appears to be your first time running this version of Splunk.

Splunk software must create an administrator account during startup. Otherwise, you cannot log in.
Create credentials for the administrator account.
Characters do not appear on the screen when you type in credentials.

Please enter an administrator username: admin
Password must contain at least:
   * 8 total printable ASCII character(s).
Please enter a new password: 
Please confirm new password: 

Splunk> Finding your faults, just like mom.

Checking prerequisites...
	Checking mgmt port [8089]: open
		Creating: /opt/splunkforwarder/var/lib/splunk
		Creating: /opt/splunkforwarder/var/run/splunk
		Creating: /opt/splunkforwarder/var/run/splunk/appserver/i18n
		Creating: /opt/splunkforwarder/var/run/splunk/appserver/modules/static/css
		Creating: /opt/splunkforwarder/var/run/splunk/upload
		Creating: /opt/splunkforwarder/var/run/splunk/search_telemetry
		Creating: /opt/splunkforwarder/var/spool/splunk
		Creating: /opt/splunkforwarder/var/spool/dirmoncache
		Creating: /opt/splunkforwarder/var/lib/splunk/authDb
		Creating: /opt/splunkforwarder/var/lib/splunk/hashDb
New certs have been generated in '/opt/splunkforwarder/etc/auth'.
	Checking conf files for problems...
	Done
	Checking default conf files for edits...
	Validating installed files against hashes from '/opt/splunkforwarder/splunkforwarder-8.1.4-17f862b42a7c-Linux-arm-manifest'
	All installed files intact.
	Done
All preliminary checks passed.

Starting splunk server daemon (splunkd)...  
Done


```




### Configure the UF to send data 
(replace 10.10.10.10 with the IP addr of your heavy fowrarder or indexer) 
```
./splunk add forward-server 10.10.10.10:9997
```

### (Optionally) Configure the UF as a deplyment client
This pemits you to control the configuration of the UF from a central location
(replace 10.10.10.10 with the IP addr of your deployment server) 
```
./splunk set deploy-poll 10.10.10.10:8089
```

### Configure the UF to start at boot

```
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo cp splunkforwarder.service /lib/systemd/system
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo chmod 644 /lib/systemd/system/splunkforwarder.service 
```
### Configure the datalogger to start at boot
```
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo cp datalogger.service /lib/systemd/system
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo chmod 644 /lib/systemd/system/datalogger.service 
```
### Configure systemmd
Now the unit files have been defined, we need to tell systemd to start it during the boot sequence:
```
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo systemctl daemon-reload
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo systemctl enable splunkforwarder.service
Created symlink /etc/systemd/system/multi-user.target.wants/splunkforwarder.service → /lib/systemd/system/splunkforwarder.service.
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo systemctl enable datalogger.service 
Created symlink /etc/systemd/system/multi-user.target.wants/datalogger.service → /lib/systemd/system/datalogger.service.
```


## Reboot !


```
sudo reboot
```

# Testing and Errors
Test with python
``` 
pi@raspberrypi:~ $ python3
Python 3.7.3 (default, Jan 22 2021, 20:04:44) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
>>> from sense_hat import SenseHat
>>> sense = SenseHat()

```

If you get this
```
File "/home/pi/Desktop/PY Sense Hat/Rainbow.py", line 2, in <module>
sense = SenseHat()
File "usr/lib/python3/dist-packages/sense_hat/sense_hat.py", line 39, in init
raise OSError ('Cannot detect %s device' % self.SENSE_HAT_FB_NAME)
OSError: Cannot detect RPi-Sense FB device
```

Try this: Edit `/boot/config.txt`

```
sudo vi /boot/config.txt
```
Add the following line at the very end.
```
dtoverlay=rpi-sense
```
Reboot.

# other stuff that may or may not help



### Link the 
Thanks to https://beaconsandwich.co.uk/2019/08/14/wlan-monitoring-splunking-on-pi/
```
sudo ln -s /lib/arm-linux-gnueabihf/ld-linux.so.3 /lib/ld-linux.so.3
```
Why? Splunk UF has been Compiled with gcc, not native RPi compiler (hypothesis - should check at some point)

If you get an error, just whack a `--force` on the end...
```
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo ln -s /lib/arm-linux-gnueabihf/ld-linux.so.3 /lib/ld-linux.so.3
ln: failed to create symbolic link '/lib/ld-linux.so.3': File exists
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo ln -s /lib/arm-linux-gnueabihf/ld-linux.so.3 /lib/ld-linux.so.3 --force
pi@raspberrypi:~/rpi-sense-hat-uf $ 
```
This is what fixes the error
```
pi@raspberrypi:/opt/splunkforwarder/bin $ ./splunk start --accept-license
bash: ./splunk: cannot execute binary file: Exec format error
pi@raspberrypi:/opt/splunkforwarder/bin $ 
```
Before and after
```
pi@raspberrypi:/lib $ ls -al ld-linux.so.3 
lrwxrwxrwx 1 root root 24 May  8 00:42 ld-linux.so.3 -> /lib/ld-linux-armhf.so.3
pi@raspberrypi:/lib $ ls -al ld-linux.so.3 
lrwxrwxrwx 1 root root 38 Oct 22 18:24 ld-linux.so.3 -> /lib/arm-linux-gnueabihf/ld-linux.so.3
pi@raspberrypi:/lib $ 
```
BTW - this didn't work for me LOL
