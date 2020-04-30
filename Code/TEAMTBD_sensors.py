# TEAMTBD_sensors.py
# This program runs locally on the Raspberry Pi.
#
# Each sensor is wired to the GPIO, and every sensor event triggers an interrupt.
# the interrupt handler will fill in an entry to an archive file, as a backup archive.
# it will also fill an entry to a buffer file, which will be retrieved by the lambda
# function deployed on the AWS platform.

import RPi.GPIO as GPIO
from datetime import datetime
from datetime import date
from threading import Timer
import os

# initialize GPIO pins 23, 24, and 25
pin_list = [23, 24, 25]
# sensor number in a list
sensor_list = ["sensor01", "sensor02"]
# unique name for each sensor
sensor_names = ["doorsw_01", "lightsw_01"]

# set up all the GPIO pins that will be used
def gpio_setup(list):
	GPIO.setmode(GPIO.BCM)
	# loop through list of GPIO pins and initialize
	for number in list:
		GPIO.setup(number, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# rename each archive file once per day so that offline records can be kept
def renameArchive(sensorList):
	datetimeNow = datetime.now()
	# get a string of the timestamp for naming the file
	timestampStr = datetimeNow.strftime("%Y%b%d%H%M%S")

	# rename each sensor's archive
	# the sensor will create a new blank archive once the existing file is renamed
	for sensor in sensorList:
		archiveStr = sensor + "_archive.txt"
		# the archive file will only be renamed if it is not empty, prevents extra file from being created at startup
		if(os.path.getsize(archiveStr) > 0):
			newArchiveStr = timestampStr + "_archive_" + sensor + ".txt"
			os.rename(archiveStr, newArchiveStr)

# set the timer for renaming the archive file once per day
def timer_setup():
	# current time and day
	xTime = datetime.today()
	# next day at 1am
	yTime = xTime.replace(day=xTime.day+1, hour=1, minute=0, second=0, microsecond=0)
	# time difference
	delta_t=yTime-xTime
	
	secs=delta_t.seconds+1
	
	# set timer for the remaining amount of seconds
	# when time is up, renameArchive function is called for the list of sensors
	t = Timer(secs, renameArchive(sensor_list))
	t.start

# set up the buffer and archive files for each sensor
def sensor_setup(sensorList):
	for sensor in sensorList:
		bufferStr = sensor + "_buffer.txt"
		archiveStr = sensor + "_archive.txt"
		# quickly open and close each file to ensure both files are empty
		f0 = open(bufferStr, 'w').close()
		f1 = open(archiveStr, 'w').close()

# callback functions
# these could potentially be merged into one function, depending on whether the callback function can handle extra arguments
# many extra arguments would be needed for sensor name, location, etc.
	
# callback function for first sensor
def sensor01_callback(channel):
	time = datetime.now()
	timeStr = time.strftime("%m/%d/%Y, %H:%M:%S")
	# clear buffer file so that only one entry exists in the file at a time
	f = open('sensor01_buffer.txt', 'w').close()
	# write the entry into each file
	with open('sensor01_buffer.txt', 'a') as file1_0:
		file1_0.write("Sensor: ")
		file1_0.write(sensor_names[0])
		file1_0.write("\nTimestamp: ")
		file1_0.write(timeStr)	
	with open('sensor01_archive.txt', 'a') as file1_1:
		file1_1.write("Sensor: ")
		file1_1.write(sensor_names[0])
		file1_1.write("\nTimestamp: ")
		file1_1.write(timeStr)
		file1_1.write('\n\n')
		
# callback function for second sensor
def sensor02_callback(channel):
	time = datetime.now()
	timeStr = time.strftime("%m/%d/%Y, %H:%M:%S")
	# clear buffer file so that only one entry exists in the file at a time
	f = open('sensor02_buffer.txt', 'w').close()
	# write the entry into each file
	with open('sensor02_buffer.txt', 'a') as file2_0:
		file2_0.write("Sensor: ")
		file2_0.write(sensor_names[1])
		file2_0.write("\nTimestamp: ")
		file2_0.write(timeStr)
	with open('sensor02_archive.txt', 'a') as file2_1:
		file2_1.write("Sensor: ")
		file2_1.write(sensor_names[1])
		file2_1.write("\nTimestamp: ")
		file2_1.write(timeStr)
		file2_1.write('\n\n')

# main code
# set up GPIO
gpio_setup(list=pin_list)
# set up sensors
sensor_setup(sensorList=sensor_list)
# set up the timer
timer_setup()

# add interrupt handlers for each sensor, with 300ms debounce
GPIO.add_event_detect(25, GPIO.FALLING, callback=sensor02_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=sensor01_callback, bouncetime=300)
		
try:
	# this part loops infinitely waiting for kill button to be pressed
	while True:
		# program will wait for falling edge of kill button
		# the interrupts will interrupt this loop and go to one of the callback functions
		GPIO.wait_for_edge(24, GPIO.FALLING)
		# if button is pressed, program will stop
		print("stopping program...")
		
# clean up GPIO if ctrl-C is pressed on the terminal
except KeyboardInterrupt:
	GPIO.cleanup()
# clean up GPIO if program ends via kill button
GPIO.cleanup()