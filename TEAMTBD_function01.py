# TEAMTBD_function01.py
# 
# This program is the code for the lambda function. It retrieves the timestamp, name, location, etc. from each of the buffer files
# and publishes it to the given topic. It has checks to ensure that only new data is published (no repeated values) and that the function
# will only publish to the topic if the file is not blank.
# It is currently configured to update for new data every second. This could be changed to be longer or shorter depending on the needed update frequency.

import logging
import platform
import sys
import os
from threading import Timer
import greengrasssdk

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Creating a greengrass core sdk client
client = greengrasssdk.client("iot-data")

# Retrieving platform information to send from Greengrass Core
my_platform = platform.platform()

# function for opening the buffer file and retrieve the timestamp information
def openSensorFile(filename):
    with open(filename, 'r') as log:
        data = log.read()
    return data

# main function that does most of the work
def greengrass_hello_world_run():
    try:
		# list of file names to read from
        sensorFiles = ["/home/pi/sensor01_buffer.txt", "/home/pi/sensor02_buffer.txt"]
        
		# read data from each file
        data1 = openSensorFile(sensorFiles[0])
        data2 = openSensorFile(sensorFiles[1])
        
		# publish to topic only if the file is not empty and the file data has changed since the last read
        if data1 != greengrass_hello_world_run.initial_value_0:
            if data1 != greengrass_hello_world_run.previous_value_1:
                client.publish(topic="teamtbd/hub", queueFullPolicy="AllOrException", payload=data1)
        if data2 != greengrass_hello_world_run.initial_value_0:
            if data2 != greengrass_hello_world_run.previous_value_2:
                client.publish(topic="teamtbd/hub", queueFullPolicy="AllOrException", payload=data2)

		# assign the new data values to the previous_value variables as a check for the next read
        greengrass_hello_world_run.previous_value_1 = data1
        greengrass_hello_world_run.previous_value_2 = data2
    
	# if any exception occurs, write an error to the logger
    except Exception as e:
        logger.error("Failed to publish message: " + repr(e))

    # asynchronously schedule this function to be run again in 5 seconds
    Timer(1, greengrass_hello_world_run).start()


# main code
#
# initialize the previous_value and initial_value variables to a blank string
# so that the lambda function will not fail when starting with a blank file
greengrass_hello_world_run.previous_value_1 = ''
greengrass_hello_world_run.previous_value_2 = ''
greengrass_hello_world_run.initial_value_0 = ''

# start executing the function above
greengrass_hello_world_run()


# this is a dummy handler and will not be invoked
# instead, the code above will be executed in an infinite loop
def function_handler(event, context):
    return
