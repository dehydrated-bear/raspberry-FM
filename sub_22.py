import socket
import sys
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/XYZ")

def on_message(client, userdata, msg):
  message = msg.payload.decode()
  print(f'Message received: {message}')
    
broker = '192.168.0.8'
client = mqtt.Client()
client.connect(broker,1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()