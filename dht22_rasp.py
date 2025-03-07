import network
import time
from machine import Pin
importn dht
import ujso
from umqtt.simple import MQTTClient

# MQTT Server Parameters
MQTT_CLIENT_ID = "micropython-weather-demo"
MQTT_BROKER    = "broker.mqttdashboard.com"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "wokwi-weather"

sensor = dht.DHT22(Pin(15))

print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Connected!")

print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()

print("Connected!")

prev_weather = ""
while True:
  
  sensor.measure() 
  message = ujson.dumps({
    "temp": sensor.temperature(),
    "humidity": sensor.humidity(),
  })
  if message != prev_weather:
    print("Updated!")
    print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC, message))
    client.publish(MQTT_TOPIC, message)
    prev_weather = message
  else:
    print("No change")
  time.sleep(1)







from time import sleep
import random
import paho.mqtt.client as mqtt

broker = '192.168.0.8'
client = mqtt.Client()
client.connect(broker,1883,60)

# Generate some random start values
x, y, z = random.random(), random.random(), random.random()

# Send a few messages
for i in range(10):

    # Publish out three values
    client.publish("topic/XYZ", f'{x},{y},{z}');

    sleep(1)
    x += 1
    y += 1
    z += 1