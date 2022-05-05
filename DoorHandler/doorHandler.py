import subprocess
import numpy as np
import cv2
import os
import time
import sys
import math
import glob
import signal
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

myMQTTClient = AWSIoTMQTTClient("Ccw_Raspi2_ID") #random key, if another connection using the same key is opened the previous one is auto closed by AWS IOT
myMQTTClient.configureEndpoint("a2vv0cnk6n1beh-ats.iot.us-east-1.amazonaws.com", 8883)

myMQTTClient.configureCredentials("../../Certificates/root-ca.pem", "../../Certificates/private.pem.key", "../../Certificates/certificate.pem.crt")

myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec
myMQTTClient.connect()
print ('Initialized Connection between current device and AWS IoT Core...')

# Subscribe Messages
def helloworld(self, params, packet):
    "Receive message from IOT console"
    print("Topic: "+packet.topic)
    # print("Payload: ",(packet.payload))
    print(packet.payload.decode("utf-8"))
    text = packet.payload.decode("utf-8")
    if text == openword1:
        print("\n===== Password recognized, Door opened for 3 sec! =====\n")

    if text == openword2:
        # Do something
        print("\n===== Face Recognized, Door opened for 3 sec! =====\n")

    if text == alarmword:
        print("\n===== System alarmed, Door has been locked =====\n")
        sys.exit(-1)

myMQTTClient.subscribe("$aws/things/k64f/shadow/update/accepted", 1, helloworld)

openword1 = "Password matched! Door open.."
openword2 = "Host, open the door"
alarmword = "=== ALARM! Suspicious identity found ==="

while True:
    time.sleep(5)
