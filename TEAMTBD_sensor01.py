import RPi.GPIO as GPIO
import datetime
from datetime import datetime
from datetime import date
from threading import Timer
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

f1_0 = open('sensor01_buffer.txt', 'w').close()
f1_1 = open('sensor01_archive.txt', 'w').close()
f2_0 = open('sensor02_buffer.txt', 'w').close()
f2_1 = open('sensor02_archive.txt', 'w').close()

try:
	xTime = datetime.today()
	yTime = xTime.replace(day=xTime.day+1, hour=1, minute=0, second=0, microsecond=0)
	delta_t=yTime-xTime

	secs=delta_t.seconds+1

	t = Timer(secs, renameArchives())
	t.start

	while True:
		GPIO.wait_for_edge(23, GPIO.FALLING)
		GPIO.wait_for_edge(25, GPIO.FALLING)
		time = datetime.now()
		timeStr = time.strftime("%m/%d/%Y, %H:%M:%S")
		f0 = open('sensor01_buffer.txt', 'w').close()
		f0 = open('sensor02_buffer.txt', 'w').close()
		with open('sensor01_buffer.txt', 'a') as file1_0:
			file1_0.write("Timestamp: ")
			file1_0.write(timeStr)	
		with open('sensor01_archive.txt', 'a') as file1_1:
			file1_1.write("Timestamp: ")
			file1_1.write(timeStr)
			file1_1.write('\n')
		with open('sensor02_buffer.txt', 'a') as file2_0:
			file2_0.write("Timestamp: ")
			file2_0.write(timeStr)
		with open('sensor02_archive.txt', 'a') as file2_1:
			file2_1.write("Timestamp: ")
			file2_1.write(timeStr)
			file2_1.write('\n')
except KeyboardInterrupt:
	GPIO.cleanup()
GPIO.cleanup()

def renameArchives():
	datetimeStr = datetime.now.strftime("%Y%m%d%H%M%S")
	newSensor1Str = datetimeStr + "_archive_sensor01.txt"
	os.rename('sensor01_archive.txt', newSensor1Str)
	newSensor2Str = datetimeStr + "_archive_sensor02.txt"
	os.rename('sensor02_archive.txt', newSensor2Str)