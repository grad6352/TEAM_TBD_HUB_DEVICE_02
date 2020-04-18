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


def openSensorFile(filename):
    with open(filename, 'r') as log:
        data = log.read()
    return data

def greengrass_hello_world_run():
    try:
        sensorFiles = ["/home/pi/sensor01_buffer.txt", "/home/pi/sensor02_buffer.txt"]
        
        data1 = openSensorFile(sensorFiles[0])
        data2 = openSensorFile(sensorFiles[1])
        
        if data1 != greengrass_hello_world_run.initial_value_0:
            if data1 != greengrass_hello_world_run.previous_value_1:
                client.publish(topic="teamtbd/hub", queueFullPolicy="AllOrException", payload=data1)
        if data2 != greengrass_hello_world_run.initial_value_0:
            if data2 != greengrass_hello_world_run.previous_value_2:
                client.publish(topic="teamtbd/hub", queueFullPolicy="AllOrException", payload=data2)
        
        greengrass_hello_world_run.previous_value_1 = data1
        greengrass_hello_world_run.previous_value_2 = data2
        
    except Exception as e:
        logger.error("Failed to publish message: " + repr(e))

    # Asynchronously schedule this function to be run again in 5 seconds
    Timer(1, greengrass_hello_world_run).start()


# Start executing the function above
greengrass_hello_world_run.previous_value_1 = ''
greengrass_hello_world_run.previous_value_2 = ''
greengrass_hello_world_run.initial_value_0 = ''

greengrass_hello_world_run()


# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return
