#!/usr/bin/python3
from sense_hat import SenseHat
from datetime import datetime
from csv import writer
import time

# SenseHat object
sense = SenseHat()

# Define some colours (R,G,B)
blue   = (0,0,255)
yellow = (255,255,0)
red    = (255,0,0)
green  = (0,255,0)
black  = (0,0,0)
white  = (255,255,255)


# Function tp sense the data
def get_sense_data():
    sense_data = []
    
    sense_data.append(datetime.now())

    sense_data.append("temperature="+str(sense.get_temperature()))
    sense_data.append("pressure="+str(sense.get_pressure()))
    sense_data.append("humidity="+str(sense.get_humidity()))

    orientation = sense.get_orientation()
    sense_data.append("yaw="+str(orientation["yaw"]))
    sense_data.append("pitch="+str(orientation["pitch"]))
    sense_data.append("roll="+str(orientation["roll"]))

    acc = sense.get_accelerometer_raw()
    sense_data.append("acc_x="+str(acc["x"]))
    sense_data.append("acc_y="+str(acc["y"]))
    sense_data.append("acc_z="+str(acc["z"]))

    gyro = sense.get_gyroscope_raw()
    sense_data.append("gyro_x="+str(gyro["x"]))
    sense_data.append("gyro_y="+str(gyro["y"]))
    sense_data.append("gyro_z="+str(gyro["z"]))

    return sense_data

# Function to display the temperature
def display_temp():
    temp = sense.get_temperature()
    
    # bug: https://github.com/astro-pi/python-sense-hat/issues/106
    #degree_sign = u"\N{DEGREE SIGN}"
    #temp_str = str(round(temp,1))+degree_sign

    temp_str = str(round(temp,1))

    # could change colour based on temperature?
    fg_colour = blue
    bg_colour = black
    sense.show_message(temp_str, text_colour=fg_colour, back_colour=bg_colour)
     
# Function to collect the data
# NB: Needs to logrotate occasionally ?
def collect_data():
    with open('data.csv', 'w', newline='') as fd:

        # open the file handle
        data_writer = writer(fd)

        # kinda forever
        while True:
            data = get_sense_data()
            data_writer.writerow(data)

            # flush the output so the UF can pick it up straight
            # away instead of waiting for the buffer to become 
            # full
            fd.flush()   

            # obvious
            display_temp()

            # sample rate
            time.sleep(10)

def run():
    collect_data()    

run()

