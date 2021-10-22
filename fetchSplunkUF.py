#!/usr/bin/python3

import os

print ("Attempting to fetch Splunk UF for ARM")
os.system("wget -O splunkforwarder-8.2.2.1-ae6821b7c64b-Linux-armv8.tgz 'https://download.splunk.com/products/universalforwarder/releases/8.2.2.1/linux/splunkforwarder-8.2.2.1-ae6821b7c64b-Linux-armv8.tgz'")
os.system("wget -O splunkforwarder-8.1.4-17f862b42a7c-Linux-arm.tgz 'https://download.splunk.com/products/universalforwarder/releases/8.1.4/linux/splunkforwarder-8.1.4-17f862b42a7c-Linux-arm.tgz'")
