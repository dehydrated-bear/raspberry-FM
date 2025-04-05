import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import paho.mqtt.client as mqtt
import json  # Import JSON for parsing the MQTT message

# Flask app setup
app = Flask(__name__)
socketio = SocketIO(app)  # Initialize Flask-SocketIO

# MQTT Broker setup
mqtt_broker = "5.196.78.28"  # MQTT Broker IP
mqtt_port = 1883  # Default MQTT port
mqtt_topic = "sensor/data"  # The topic to subscribe to

# Global variables to store temperature and humidity
temperature = None
humidity = None

# Callback when the MQTT client receives a message
def on_message(client, userdata, msg):
    global temperature, humidity
    # Parse the message payload into JSON
    try:
        data = json.loads(msg.payload.decode('utf-8'))  # Decode and load the JSON message
        temperature = data.get('temperature')  # Get the temperature from the JSON data
        humidity = data.get('humidity')  # Get the humidity from the JSON data
        
        # Emit the updated data to the client-side via SocketIO
        socketio.emit('sensor_data', {'temperature': temperature, 'humidity': humidity})
        print(f"Received JSON data: {data}")  # Optionally print the data for debugging
    except json.JSONDecodeError:
        print("Failed to decode JSON message")
    except Exception as e:
        print(f"Error processing message: {e}")

# MQTT client setup
client = mqtt.Client()
client.on_message = on_message

# Connect to the MQTT broker and subscribe to the topic
def connect_mqtt():
    client.connect(mqtt_broker, mqtt_port, 60)
    client.subscribe(mqtt_topic)
    client.loop_start()  # Start the MQTT loop in a background thread

# Flask route for the homepage
@app.route('/')
def home():
    return render_template('index.html')  # Render the index.html page

# Start the Flask application
if __name__ == '__main__':
    connect_mqtt()  # Connect to MQTT broker
    socketio.run(app, debug=True)  # Run the Flask app with SocketIO
