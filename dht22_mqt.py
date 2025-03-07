import time
import Adafruit_DHT
import paho.mqtt.client as mqtt


sensor = Adafruit_DHT.DHT22
gpio_pin = 4  


mqtt_broker = "localhost" 
mqtt_port = 1883
mqtt_topic = "home/sensors/dht22"


client = mqtt.Client()


client.connect(mqtt_broker, mqtt_port, 60)


while True:
    
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio_pin)

    if humidity is not None and temperature is not None:
       
        message = f"Temperature: {temperature}C, Humidity: {humidity}%"
        print(message)

        
        client.publish(mqtt_topic, message)
    else:
        print("Failed to retrieve data from sensor")

    time.sleep(10) 
