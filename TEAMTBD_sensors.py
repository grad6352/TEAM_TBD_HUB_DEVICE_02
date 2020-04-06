import RPi.GPIO as GPIO
#import datetime
from datetime import datetime
from datetime import date
from threading import Timer
import os

pin_list = [23, 24, 25]
sensor_list = ["sensor01", "sensor02"]

def gpio_setup(list):
	GPIO.setmode(GPIO.BCM)
	for number in list:
		GPIO.setup(number, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def renameArchive(sensorList):
	datetimeNow = datetime.now()
	timestampStr = datetimeNow.strftime("%Y%b%d%H%M%S")

	for sensor in sensorList:
		archiveStr = sensor + "_archive.txt"
		if(os.path.getsize(archiveStr) > 0):
			newArchiveStr = timestampStr + "_archive_" + sensor + ".txt"
			os.rename(archiveStr, newArchiveStr)

def timer_setup():
	xTime = datetime.today()
	yTime = xTime.replace(day=xTime.day+1, hour=1, minute=0, second=0, microsecond=0)
	delta_t=yTime-xTime
	
	secs=delta_t.seconds+1
	
	t = Timer(secs, renameArchive(sensor_list))
	t.start

def sensor_setup(sensorList):
	for sensor in sensorList:
		bufferStr = sensor + "_buffer.txt"
		archiveStr = sensor + "_archive.txt"
		f0 = open(bufferStr, 'w').close()
		f1 = open(archiveStr, 'w').close()
		
def sensor01_callback(channel):
	time = datetime.now()
	timeStr = time.strftime("%m/%d/%Y, %H:%M:%S")
	f = open('sensor01_buffer.txt', 'w').close()
	with open('sensor01_buffer.txt', 'a') as file1_0:
		file1_0.write("Timestamp: ")
		file1_0.write(timeStr)	
	with open('sensor01_archive.txt', 'a') as file1_1:
		file1_1.write("Timestamp: ")
		file1_1.write(timeStr)
		file1_1.write('\n')
		
def sensor02_callback(channel):
	time = datetime.now()
	timeStr = time.strftime("%m/%d/%Y, %H:%M:%S")
	f = open('sensor02_buffer.txt', 'w').close()
	with open('sensor02_buffer.txt', 'a') as file2_0:
		file2_0.write("Timestamp: ")
		file2_0.write(timeStr)
	with open('sensor02_archive.txt', 'a') as file2_1:
		file2_1.write("Timestamp: ")
		file2_1.write(timeStr)
		file2_1.write('\n')

gpio_setup(list=pin_list)
sensor_setup(sensorList=sensor_list)
timer_setup()

GPIO.add_event_detect(25, GPIO.FALLING, callback=sensor02_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=sensor01_callback, bouncetime=300)
		
try:
	while True:
		GPIO.wait_for_edge(24, GPIO.FALLING)
		print("stopping program...")		
except KeyboardInterrupt:
	GPIO.cleanup()
GPIO.cleanup()