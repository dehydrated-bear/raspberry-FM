import sqlite3
import paho.mqtt.client as mqtt

mqtt_broker = "192.168.1.100"
mqtt_port = 1883
mqtt_topic = "home/sensors/dht22"

def store_data(temperature, humidity):
    conn = sqlite3.connect('mqtt_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO sensor_data (temperature, humidity)
    VALUES (?, ?)
    ''', (temperature, humidity))
    conn.commit()
    conn.close()

def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    print(f"Received message: {payload}")
    
    try:
        temp_str, humidity_str = payload.split(", ")
        temperature = float(temp_str.split(":")[1].strip('C'))
        humidity = float(humidity_str.split(":")[1].strip('%'))
        store_data(temperature, humidity)
    except Exception as e:
        print(f"Error processing message: {e}")

client = mqtt.Client()
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port, 60)
client.subscribe(mqtt_topic)
client.loop_forever()
