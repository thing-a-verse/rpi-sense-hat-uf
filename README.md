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
```
$ wget -O splunkforwarder-8.2.2.1-ae6821b7c64b-Linux-armv8.tgz 'https://download.splunk.com/products/universalforwarder/releases/8.2.2.1/linux/splunkforwarder-8.2.2.1-ae6821b7c64b-Linux-armv8.tgz'
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

```
pi@raspberrypi:~/rpi-sense-hat-uf $ sudo tar -xvsf splunkforwarder-8.2.2.1-ae6821b7c64b-Linux-armv8.tgz -C /opt

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

### Link
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


### ChangeDir to $SPLUNK_HOME/bin
```
pi@raspberrypi:~ $ cd $SPLUNK_HOME/bin
pi@raspberrypi:/opt/splunkforwarder/bin $
```

### Now accept the EULA
```
./splunk start --accept-license
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


### Configure the datalogger to start at boot


## Reboot !




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

