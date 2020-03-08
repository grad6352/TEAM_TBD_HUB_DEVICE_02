import RPi.GPIO as GPIO
import datetime

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Waiting for MAHIVE event on port 23")

try:
	f1 = open('textlog.txt', 'w+')
	f1.close()
	while True:
		GPIO.wait_for_edge(23, GPIO.FALLING)
		print("\nMAHIVE event detected")
		time = datetime.datetime.now()
		timeStr = time.strftime("%m/%d/%Y, %H:%M:%S")
		with open('textlog.txt', 'a') as file1:
			file1.write("\nTimestamp: ")
			file1.write(timeStr)	
except KeyboardInterrupt:
	GPIO.cleanup()
GPIO.cleanup()
#file1.close()
	
