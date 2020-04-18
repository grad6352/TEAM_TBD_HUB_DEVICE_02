#
# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

# greengrassHelloWorld.py
# Demonstrates a simple publish to a topic using Greengrass core sdk
# This lambda function will retrieve underlying platform information and send
# a hello world message along with the platform information to the topic
# 'hello/world'. The function will sleep for five seconds, then repeat.
# Since the function is long-lived it will run forever when deployed to a
# Greengrass core.  The handler will NOT be invoked in our example since
# the we are executing an infinite loop.

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


# When deployed to a Greengrass core, this code will be executed immediately
# as a long-lived lambda function.  The code will enter the infinite while
# loop below.
# If you execute a 'test' on the Lambda Console, this test will fail by
# hitting the execution timeout of three seconds.  This is expected as
# this function never returns a result.
def openSensorFile(filename):
    with open(filename, 'r') as log:
        data = log.read()
    return data

def greengrass_hello_world_run():
    try:
        #if not my_platform:
        #    client.publish(
        #        topic="hello/world", queueFullPolicy="AllOrException", payload="Hello world! Sent from Greengrass Core."
        #    )
        #else:
        #    client.publish(
        #        topic="hello/world",
        #        queueFullPolicy="AllOrException",
        #        payload="Hello world! Sent from " "Greengrass Core running on platform: {}".format(my_platform),
        #    )
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
        
        #for sensor in sensorFiles:
        #    with open(sensor, 'r') as log:
        #        data1 = log.read()
        #    if data1 != greengrass_hello_world_run.previous_value_1:
        #        if data1 != greengrass_hello_world_run.previous_value_2:
        #            if data1 != greengrass_hello_world_run.initial_value:
        #                client.publish(topic="teamtbd/hub", queueFullPolicy="AllOrException", payload=data1)
        #                if sensor == sensors[0]:
        #                    greengrass_hello_world_run.previous_value_1 = data1
        #                else if sensor == sensors[1]
        #                    greengrass_hello_world_run.previous_value_2 = data1
        #            else
        #                client.publish(topic="teamtbd/hub", queueFullPolicy="AllOrException", payload="foo")
        #    greengrass_hello_world_run.previous_value = data
    except Exception as e:
        logger.error("Failed to publish message: " + repr(e))

    # Asynchronously schedule this function to be run again in 5 seconds
    Timer(5, greengrass_hello_world_run).start()


# Start executing the function above
greengrass_hello_world_run.previous_value_1 = ''
greengrass_hello_world_run.previous_value_2 = ''
greengrass_hello_world_run.initial_value_0 = ''

greengrass_hello_world_run()


# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return
