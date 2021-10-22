# rpi-sense-hat-uf
Raspberry Pi - Sense Hat to Splunk UF

# Install
`sudo apt-get install sense-hat`

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

