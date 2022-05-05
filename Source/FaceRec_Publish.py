#!/bin/bash
import subprocess
import numpy as np
import cv2
import os
import time
import sys
import math
import glob
import signal
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from FaceRecLib import Face_Recognition

def publish_host():
    # Publish one Message
    myMQTTClient.publish(
        topic="$aws/things/k64f/shadow/update/accepted",
        QoS=1,
        payload="Host, open the door")

    print("Published message to the topic!")

def publish_unknown():
    # Publish one Message
    myMQTTClient.publish(
        topic="$aws/things/k64f/shadow/update/accepted",
        QoS=1,
        payload="Unknown person!")

    print("Published message to the topic!")

myMQTTClient = AWSIoTMQTTClient("Ccw_Mac_ID") #random key, if another connection using the same key is opened the previous one is auto closed by AWS IOT
myMQTTClient.configureEndpoint("a2vv0cnk6n1beh-ats.iot.us-east-1.amazonaws.com", 8883)

myMQTTClient.configureCredentials("../../Certificates/root-ca.pem", "../../Certificates/private.pem.key", "../../Certificates/certificate.pem.crt")

myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec
myMQTTClient.connect()
print ('Initialized Connection between current device and AWS IoT Core...')

# Clear text file
f = open('face_result.txt', 'r+')
f.truncate(0)

lines = ["Host", "Unknown person"]

# Run Face recognition 
obj = Face_Recognition()
host = obj.main()

if (host):
	publish_host()

elif (host == False):
	publish_unknown()

else:
	print("No person recognized")