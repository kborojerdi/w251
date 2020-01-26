# Header

import numpy as np
import cv2
import paho.mqtt.client as mqtt
import binascii

# print("test")
# image = cv2.imread("/mnt/mybucket/test.png")
# print(binascii.hexlify(image))
# cv2.imwrite("/mnt/mybucket/face.png", image)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
   print("Connected with result code "+str(rc))

   # Subscribing in on_connect() means that if we lose the connection and
   # reconnect then subscriptions will be renewed.
   client.subscribe("test")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
   msg = msg.payload
   
   print("message recieved")
   print("length")
   print(len(msg))
   #print(binascii.hexlify(msg))

   face = np.frombuffer(msg, dtype=np.uint8)
   image = cv2.imdecode(face, flags=0)
   # print(image.shape)
   print("test")

   cv2.imwrite("/mnt/mybucket/myface.png", image)
   print("image written")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mosquitto", 1883, 300)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
