# rpi-sense-hat-uf
Raspberry Pi - Sense Hat to Splunk UF

# Installation
## Install the sense-hat libraries for RPi. 
It is probably already installed, but if not ...
```bash
pi@raspberrypi:~ $ sudo apt-get install sense-hat
```

## Clone this repo
```bash
pi@raspberrypi:~ $ git clone https://github.com/thing-a-verse/rpi-sense-hat-uf.git
```


## Start the sensor
In a terminal window, Start the sensor
```bash
pi@raspberrypi:~ $ cd rpi-sense-hat-uf
pi@raspberrypi:~/rpi-sense-hat-uf $ ./datalogger.py
```

In another terminal windows, Check the data is being generated. If it's working you'll also see
the temperature displayed on the LED display
```bash
pi@raspberrypi:~ $ cd rpi-sense-hat-uf
pi@raspberrypi:~/rpi-sense-hat-uf $ tail -f data.csv
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
```bash
pi@raspberrypi:~/rpi-sense-hat-uf $ wget -O splunkforwarder-8.2.2.1-ae6821b7c64b-Linux-armv8.tgz 'https://download.splunk.com/products/universalforwarder/releases/8.2.2.1/linux/splunkforwarder-8.2.2.1-ae6821b7c64b-Linux-armv8.tgz'
```
or, if you have an RPi 3 ... get the older ARMv6 code from v8.1.4
```bash
pi@raspberrypi:~/rpi-sense-hat-uf $ wget -O splunkforwarder-8.1.4-17f862b42a7c-Linux-arm.tgz 'https://download.splunk.com/products/universalforwarder/releases/8.1.4/linux/splunkforwarder-8.1.4-17f862b42a7c-Linux-arm.tgz'
```
### Method 3
Run the fetch program
```bash
pi@raspberrypi:~/rpi-sense-hat-uf $ ./fetchSplunkUF.py
```
# Install the UF

Try [reading the fine manuals](https://docs.splunk.com/Documentation/Forwarder/8.2.2/Forwarder/Abouttheuniversalforwarder)
Specifically: [Installation](https://docs.splunk.com/Documentation/Forwarder/8.2.2/Forwarder/Installanixuniversalforwarder)

or

### Install it as the pi user as follows
RPi 4...
```bash
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo tar -xvsf splunkforwarder-8.2.2.1-ae6821b7c64b-Linux-armv8.tgz -C /opt

```
RPi 3...
```bash
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo tar -xvsf splunkforwarder-8.1.4-17f862b42a7c-Linux-arm.tgz -C /opt
```



Per the fine manuals, it's not best practice to run Splunk as root
https://docs.splunk.com/Documentation/Splunk/8.2.2/Installation/RunSplunkasadifferenttornon-rootuser

```bash
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo chown -R pi:pi /opt/splunkforwarder/

```

### Configure $SPLUNK_HOME
```bash
pi@raspberrypi:~/rpi-sense-hat-uf $ vi ~/.profile 
```
Add the following to the bottom
```bash
export SPLUNK_HOME=/opt/splunkforwarder
export PATH=$PATH:$SPLUNK_HOME/bin
```
Don't forget to re-source the `.profile` (or close the terminal windows and re-open a new one)
```bash
pi@raspberrypi:~/rpi-sense-hat-uf $ . ~/.profile
pi@raspberrypi:~/rpi-sense-hat-uf $ echo $SPLUNK_HOME
/opt/splunkforwarder
pi@raspberrypi:~/rpi-sense-hat-uf $ 
```



### ChangeDir to $SPLUNK_HOME/bin
```bash
pi@raspberrypi:~ $ cd $SPLUNK_HOME/bin
pi@raspberrypi:/opt/splunkforwarder/bin $
```

### Now accept the EULA
```bash
./splunk start --accept-license
```

> [!TIP]
> If you get the error `bash: ./splunk: cannot execute binary file: Exec format error`, you installed the wrong version on your RPI 3

Backtrack as follows
```bash
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo rm -rf /opt/splunkforwarder
pi@raspberrypi:~/rpi-sense-hat-uf $ wget -O splunkforwarder-8.1.4-17f862b42a7c-Linux-arm.tgz 'https://download.splunk.com/products/universalforwarder/releases/8.1.4/linux/splunkforwarder-8.1.4-17f862b42a7c-Linux-arm.tgz'
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo tar -xvsf splunkforwarder-8.1.4-17f862b42a7c-Linux-arm.tgz -C /opt
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo chown -R pi:pi /opt/splunkforwarder/
pi@raspberrypi:~ $ cd $SPLUNK_HOME/bin
./splunk start --accept-license
```

If successful, you'll see
```bash
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


Splunk should start
```bash
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
(replace 10.10.10.10 with the IP addr of your heavy forwarder or indexer) 

Since `$SPLUNK_HOME` is in the path, we can run this from any directory.
```bash
pi@raspberrypi:~ $ splunk add forward-server 10.10.10.10:9997
```
To display your config
```bash
pi@raspberrypi:~ $ splunk list forward-server
```
To delete it if you made a mistake
```bash
pi@raspberrypi:~ $ splunk remove forward-server 10.10.10.10:9997
```

### (Optionally) Configure the UF as a deployment client
This pemits you to control the configuration of the UF from a central location
(replace 10.10.10.10 with the IP addr of your deployment server) 
```bash
pi@raspberrypi:~ $ splunk set deploy-poll 10.10.10.10:8089
```


### Configure the UF to read our logfile
> [!IMPORTANT]
> Don't miss this step, or you won't log anything


```bash
pi@raspberrypi:~/rpi-sense-hat-uf $ cp inputs.conf $SPLUNK_HOME/etc/system/local
```

The configuration is
```bash
[monitor:///home/pi/rpi-sense-hat-uf/data.csv]
sourcetype=rpi-sense-hat
index=rpi 
```

You might like to check the `inputs.conf` file doesn't already exist, and merge your content if it does, but as this is a fresh install, it should not yet exist.
> [!TIP]
> Always put your configs into `../local`, not `../default` which is tempting, but wrong.

### Configure the UF to start at boot

```bash
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo cp splunkforwarder.service /lib/systemd/system
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo chmod 644 /lib/systemd/system/splunkforwarder.service 
```
### Configure the datalogger to start at boot
```bash
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo cp datalogger.service /lib/systemd/system
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo chmod 644 /lib/systemd/system/datalogger.service 
```
### Configure systemd
Now the unit files have been defined, we need to tell systemd to start it during the boot sequence:
```bash
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo systemctl daemon-reload
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo systemctl enable splunkforwarder.service
Created symlink /etc/systemd/system/multi-user.target.wants/splunkforwarder.service → /lib/systemd/system/splunkforwarder.service.
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo systemctl enable datalogger.service 
Created symlink /etc/systemd/system/multi-user.target.wants/datalogger.service → /lib/systemd/system/datalogger.service.
```


## Reboot !


```bash
pi@raspberrypi:~ $ sudo reboot
```

# Testing for Success
If it's working, there should be a temp on the display every 10 seconds.

### Is splunk running?
```bash
pi@raspberrypi:~/rpi-sense-hat-uf $ splunk status
splunkd is running (PID: 543).
splunk helpers are running (PIDs: 974).
pi@raspberrypi:~/rpi-sense-hat-uf $
```
### Is splunk reading my file
```bash
pi@raspberrypi:~/rpi-sense-hat-uf $ splunk list inputstatus
Your session is invalid.  Please login.
Splunk username: admin
Password: 
Cooked:tcp :
	tcp

Raw:tcp :
	tcp

TailingProcessor:FileStatus :
	$SPLUNK_HOME/etc/splunk.version
		file position = 67
		file size = 67
		percent = 100.00
		type = open file

	$SPLUNK_HOME/var/log/splunk
		type = directory

	$SPLUNK_HOME/var/log/splunk/metrics.log
		type = directory

	$SPLUNK_HOME/var/log/splunk/splunk_instrumentation_cloud.log*
		type = directory

	$SPLUNK_HOME/var/log/splunk/splunkd.log
		type = directory

	$SPLUNK_HOME/var/log/watchdog/watchdog.log*
		type = directory

	$SPLUNK_HOME/var/run/splunk/search_telemetry/*search_telemetry.json
		type = directory

	$SPLUNK_HOME/var/spool/splunk/...stash_new
		type = directory

	/home/pi/rpi-sense-hat-uf/data.csv
		file position = 347
		file size = 347
		percent = 100.00
		type = open file

	/opt/splunkforwarder/var/log/splunk/audit.log
		file position = 74174
		file size = 74174
		parent = $SPLUNK_HOME/var/log/splunk
		percent = 100.00
		type = open file

	/opt/splunkforwarder/var/log/splunk/btool.log
		file position = 0
		file size = 0
		parent = $SPLUNK_HOME/var/log/splunk
		percent = 100
		type = finished reading

	/opt/splunkforwarder/var/log/splunk/conf.log
		file position = 1615
		file size = 1615
		parent = $SPLUNK_HOME/var/log/splunk
		percent = 100.00
		type = open file

	/opt/splunkforwarder/var/log/splunk/dfm_stderr.log
		file position = 0
		file size = 0
		parent = $SPLUNK_HOME/var/log/splunk
		percent = 100
		type = finished reading

	/opt/splunkforwarder/var/log/splunk/dfm_stdout.log
		file position = 0
		file size = 0
		parent = $SPLUNK_HOME/var/log/splunk
		percent = 100
		type = finished reading

	/opt/splunkforwarder/var/log/splunk/first_install.log
		file position = 67
		file size = 67
		parent = $SPLUNK_HOME/var/log/splunk
		percent = 100.00
		type = open file

	/opt/splunkforwarder/var/log/splunk/health.log
		file position = 11407
		file size = 11407
		parent = $SPLUNK_HOME/var/log/splunk
		percent = 100.00
		type = open file

	/opt/splunkforwarder/var/log/splunk/license_usage.log
		file position = 0
		file size = 0
		parent = $SPLUNK_HOME/var/log/splunk
		percent = 100
		type = finished reading

	/opt/splunkforwarder/var/log/splunk/metrics.log
		file position = 786432
		file size = 1517351
		parent = $SPLUNK_HOME/var/log/splunk/metrics.log
		percent = 51.83
		type = open file

	/opt/splunkforwarder/var/log/splunk/mongod.log
		file position = 0
		file size = 0
		parent = $SPLUNK_HOME/var/log/splunk
		percent = 100
		type = finished reading

	/opt/splunkforwarder/var/log/splunk/remote_searches.log
		file position = 0
		file size = 0
		parent = $SPLUNK_HOME/var/log/splunk
		percent = 100
		type = finished reading

	/opt/splunkforwarder/var/log/splunk/scheduler.log
		file position = 0
		file size = 0
		parent = $SPLUNK_HOME/var/log/splunk
		percent = 100
		type = finished reading

	/opt/splunkforwarder/var/log/splunk/search_messages.log
		file position = 0
		file size = 0
		parent = $SPLUNK_HOME/var/log/splunk
		percent = 100
		type = finished reading

	/opt/splunkforwarder/var/log/splunk/searchhistory.log
		file position = 0
		file size = 0
		parent = $SPLUNK_HOME/var/log/splunk
		percent = 100
		type = finished reading

	/opt/splunkforwarder/var/log/splunk/splunk_instrumentation_cloud.log
		file position = 0
		file size = 0
		parent = $SPLUNK_HOME/var/log/splunk/splunk_instrumentation_cloud.log*
		percent = 100
		type = finished reading

	/opt/splunkforwarder/var/log/splunk/splunkd-utility.log
		file position = 5555
		file size = 5555
		parent = $SPLUNK_HOME/var/log/splunk
		percent = 100.00
		type = open file

	/opt/splunkforwarder/var/log/splunk/splunkd.log
		file position = 200248
		file size = 199159
		parent = $SPLUNK_HOME/var/log/splunk/splunkd.log
		percent = 100.55
		type = open file

	/opt/splunkforwarder/var/log/splunk/splunkd_access.log
		file position = 759
		file size = 759
		parent = $SPLUNK_HOME/var/log/splunk
		percent = 100.00
		type = open file

	/opt/splunkforwarder/var/log/splunk/splunkd_stderr.log
		file position = 1262
		file size = 1262
		parent = $SPLUNK_HOME/var/log/splunk
		percent = 100.00
		type = open file

	/opt/splunkforwarder/var/log/splunk/splunkd_stdout.log
		file position = 0
		file size = 0
		parent = $SPLUNK_HOME/var/log/splunk
		percent = 100
		type = finished reading

	/opt/splunkforwarder/var/log/splunk/splunkd_ui_access.log
		file position = 0
		file size = 0
		parent = $SPLUNK_HOME/var/log/splunk
		percent = 100
		type = finished reading

	/opt/splunkforwarder/var/log/splunk/wlm_monitor.log
		file position = 0
		file size = 0
		parent = $SPLUNK_HOME/var/log/splunk
		percent = 100
		type = finished reading

pi@raspberrypi:~/rpi-sense-hat-uf $ 
```

There it is:
```
        /home/pi/rpi-sense-hat-uf/data.csv
                file position = 347
                file size = 347
                percent = 100.00
                type = open file
```



# Testing and Errors
Test with python
```bash
pi@raspberrypi:~ $ python3
Python 3.7.3 (default, Jan 22 2021, 20:04:44) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
>>> from sense_hat import SenseHat
>>> sense = SenseHat()

```

If you get this
```bash
File "/home/pi/Desktop/PY Sense Hat/Rainbow.py", line 2, in <module>
sense = SenseHat()
File "usr/lib/python3/dist-packages/sense_hat/sense_hat.py", line 39, in init
raise OSError ('Cannot detect %s device' % self.SENSE_HAT_FB_NAME)
OSError: Cannot detect RPi-Sense FB device
```

Try this: Edit `/boot/config.txt`

```bash
pi@raspberrypi:~ $ sudo vi /boot/config.txt
```
Add the following line at the very end.
```conf
dtoverlay=rpi-sense
```
Reboot.

# other stuff that may or may not help



### Link the 
Thanks to https://beaconsandwich.co.uk/2019/08/14/wlan-monitoring-splunking-on-pi/
```bash
sudo ln -s /lib/arm-linux-gnueabihf/ld-linux.so.3 /lib/ld-linux.so.3
```
Why? Splunk UF has been Compiled with gcc, not native RPi compiler (hypothesis - should check at some point)

If you get an error, just whack a `--force` on the end...
```bash
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo ln -s /lib/arm-linux-gnueabihf/ld-linux.so.3 /lib/ld-linux.so.3
ln: failed to create symbolic link '/lib/ld-linux.so.3': File exists
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo ln -s /lib/arm-linux-gnueabihf/ld-linux.so.3 /lib/ld-linux.so.3 --force
pi@raspberrypi:~/rpi-sense-hat-uf $ 
```
This is what fixes the error
```bash
pi@raspberrypi:/opt/splunkforwarder/bin $ ./splunk start --accept-license
bash: ./splunk: cannot execute binary file: Exec format error
pi@raspberrypi:/opt/splunkforwarder/bin $ 
```
Before and after
```bash
pi@raspberrypi:/lib $ ls -al ld-linux.so.3 
lrwxrwxrwx 1 root root 24 May  8 00:42 ld-linux.so.3 -> /lib/ld-linux-armhf.so.3
pi@raspberrypi:/lib $ ls -al ld-linux.so.3 
lrwxrwxrwx 1 root root 38 Oct 22 18:24 ld-linux.so.3 -> /lib/arm-linux-gnueabihf/ld-linux.so.3
pi@raspberrypi:/lib $ 
```
BTW - this didn't work for me LOL

# Time and date
So - the data is in Splunk - but the time is wrong??

Probably you need to get NTP or timedatectl working. Here's an example of correctly configured `timedatectl`:

```bash
pi@raspberrypi:~ $ timedatectl status
               Local time: Mon 2021-10-25 11:15:36 AEDT
           Universal time: Mon 2021-10-25 00:15:36 UTC
                 RTC time: n/a
                Time zone: Australia/Sydney (AEDT, +1100)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
pi@raspberrypi:~ $ date
Mon 25 Oct 2021 11:15:51 AM AEDT
```

If this incorrect (e.g. it reads `inactive` or synchronised is `no`)

Locate your NTP server and make sure you can ping it.

## Use `timedatectl`

Locate your timezone (e.g. Sydney)
```bash
pi@raspberrypi:~ $ sudo timedatectl list-timezones | grep Sydney
Australia/Sydney
pi@raspberrypi:~ $
```
Then set this timezone
```bash
pi@raspberrypi:~ $ sudo timedatectl set-timezone Australia/Sydney
pi@raspberrypi:~ $
```
Edit `timesyncd.conf`
```bash
pi@raspberrypi:~ $ sudo vi /etc/systemd/timesyncd.conf
pi@raspberrypi:~ $
```
Configure your NTP server in the clause `NTP=`

```conf
#  This file is part of systemd.
#
#  systemd is free software; you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.
#
# Entries in this file show the compile time defaults.
# You can change settings by editing this file.
# Defaults can be restored by simply deleting this file.
#
# See timesyncd.conf(5) for details.

[Time]
NTP=10.10.10.1
Fallback=10.10.10.2
#FallbackNTP=0.debian.pool.ntp.org 1.debian.pool.ntp.org 2.debian.pool.ntp.org 3.debian.pool.ntp.org
RootDistanceMaxSec=5
PollIntervalMinSec=32
PollIntervalMaxSec=2048
```

Restart NTP (seems superfluous ?)
```bash
pi@raspberrypi:~ $ sudo service ntp restart
pi@raspberrypi:~ $
```


and reboot...
```bash
pi@raspberrypi:~ $ sudo reboot
```


> [!TIP]
> It takes a bit of time to sync, but once it's working you see `synchronised:yes`


## Use `NTP`

```bash
sudo apt install ntp
```

The fine manuals will explain how to configure it, but you ought to be fine with `timedatectl` above.
