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
from FaceRecLib import Face_Recognition


def voiceRecognition_start():
    global p1
    rpistr_voice = "../Voice_Recognition/voice2text.sh"
    p1 = subprocess.Popen(rpistr_voice, shell=True, preexec_fn=os.setsid)

def faceRecognition_start():
    global p
    rpistr_face = "./start_face.sh"
    p = subprocess.Popen(rpistr_face, shell=True, preexec_fn=os.setsid)

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

def publish_alarm():
    # Publish one Message
    myMQTTClient.publish(
        topic="$aws/things/k64f/shadow/update/accepted",
        QoS=1,
        payload="=== ALARM! Suspicious identity found ===")

    print("Published ALARM message to the topic!")

myMQTTClient = AWSIoTMQTTClient("Ccw_Raspi1_ID") #random key, if another connection using the same key is opened the previous one is auto closed by AWS IOT
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
    if text == faceword:
        # Do something
        faceRecognition_start()
    elif text == voiceword:
        voiceRecognition_start()
    elif text == pwdLimitWord:
        publish_alarm()

myMQTTClient.subscribe("$aws/things/k64f/shadow/update/accepted", 1, helloworld)

faceword = "face recognition"
voiceword = "voice recognition"
pwdLimitWord = "Wrong password.."

while True:
    time.sleep(5)
