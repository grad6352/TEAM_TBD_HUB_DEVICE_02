import RPi.GPIO as GPIO
import datetime

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#print("Waiting for MAHIVE event on port 23")

try:
	f1 = open('button_demo_buffer.txt', 'w').close()
	f = open('button_demo_archive.txt', 'w').close()
	while True:
		GPIO.wait_for_edge(23, GPIO.FALLING)
		#print("\nMAHIVE event detected")
		time = datetime.datetime.now()
		timeStr = time.strftime("%m/%d/%Y, %H:%M:%S")
		f = open('button_demo_buffer.txt', 'w').close()
		with open('button_demo_buffer.txt', 'a') as file1:
			file1.write("Timestamp: ")
			file1.write(timeStr)	
		with open('button_demo_archive.txt', 'a') as file2:
			file2.write("Timestamp: ")
			file2.write(timeStr)
			file2.write('\n')
except KeyboardInterrupt:
	GPIO.cleanup()
GPIO.cleanup()

	
