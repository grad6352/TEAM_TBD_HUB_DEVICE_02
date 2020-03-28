import RPi.GPIO as GPIO
import datetime
from datetime import datetime
from threading import Timer
import os

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#print("Waiting for MAHIVE event on port 23")

try:
	xTime = datetime.today()
	
	f1 = open('sensor01_buffer.txt', 'w').close()
	f = open('sensor01_archive.txt', 'w').close()
	while True:
		GPIO.wait_for_edge(23, GPIO.FALLING)
		time = datetime.now()
		timeStr = time.strftime("%m/%d/%Y, %H:%M:%S")
		f = open('sensor01_buffer.txt', 'w').close()
		with open('sensor01_buffer.txt', 'a') as file1:
			file1.write("Timestamp: ")
			file1.write(timeStr)	
		with open('sensor01_archive.txt', 'a') as file2:
			file2.write("Timestamp: ")
			file2.write(timeStr)
			file2.write('\n')
except KeyboardInterrupt:
	GPIO.cleanup()
GPIO.cleanup()

def renameArchive():
	dateStr = datetime.
	os.rename('sensor01_archive.txt', 
