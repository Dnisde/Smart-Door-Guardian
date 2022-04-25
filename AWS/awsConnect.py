import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

myMQTTClient = AWSIoTMQTTClient("Ccw_Mac_ID") #random key, if another connection using the same key is opened the previous one is auto closed by AWS IOT
myMQTTClient.configureEndpoint("a1fj7nohpko3eg-ats.iot.us-east-1.amazonaws.com", 8883)

myMQTTClient.configureCredentials("./root-ca.pem", "./private.pem.key", "./certificate.pem.crt")

myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec
myMQTTClient.connect()
print ('Initiating Connection between current device and AWS IoT Core...')

# Subscribe Messages
def helloworld(self, params, packet):
	"Receive message from IOT console"
	print("Topic: "+packet.topic)
	# print("Payload: ",(packet.payload))
	print(packet.payload)
	
myMQTTClient.subscribe("home/ec544", 1, helloworld)
    
while True:
	time.sleep(5)

# Publish one Message
myMQTTClient.publish(
	topic="home/ec544",
	QoS=1,
	payload="This is Ccw's MAC"
	)
print("Published message to the topic!")