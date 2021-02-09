#!/usr/bin/python
import sys
import Adafruit_DHT
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


myMQTTClient = AWSIoTMQTTClient("RaspiTempAndHumidity") #random key, if another connection using the same key is opened the previous one is auto closed by AWS IOT
myMQTTClient.configureEndpoint("xxx", 8883)
myMQTTClient.configureCredentials("/home/pi/tempandhumidity-AWSIoT/root-ca.pem", "/home/pi/tempandhumidity-AWSIoT/private.pem.key", "/home/pi/tempandhumidity-AWSIoT/certificate.pem.crt")

myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec

myMQTTClient.connect()


def readAndPublish:
    while True:
        # humidity, temperature = Adafruit_DHT.read_retry(11, 4)
        humidity, temperature = (1,2)

        myMQTTClient.publish(
            topic="RaspiTempAndHumidity/Temperature",
            QoS=1,
            payload='{"Temperature":"'+str(temperature)+'"}'
        )

        myMQTTClient.publish(
            topic="RaspiTempAndHumidity/Humidity",
            QoS=1,
            payload='{"Humidity":"'+str(humidity)+'"}'
        )

        print("Temp: {0:0.1f} C  Humidity: {1:0.1f} %".format(temperature, humidity))


if __name__ == '__main__':
    readAndPublish()