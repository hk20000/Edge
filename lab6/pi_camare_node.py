import paho.mqtt.client as mqtt
import cv2
import base64
import time

# Topics
REQUEST_TOPIC = "camera/request"
IMAGE_TOPIC = "camera/image"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Pi Camera Node connected to MQTT broker.")
        # Subscribe to the topic where capture requests come in
        client.subscribe(REQUEST_TOPIC)
        print(f"Subscribed to '{REQUEST_TOPIC}'")
    else:
        print(f"Failed to connect. Return code: {rc}")

def on_message(client, userdata, message):
    try:
        payload = message.payload.decode().strip().lower()
        print(f"Received request message: '{payload}' on topic '{message.topic}'")

        if payload == "capture":
            # Capture image from webcam
            cap = cv2.VideoCapture(0)  # 0 is default webcam device index
            ret, frame = cap.read()
            cap.release()

            if ret:
                # Encode the image to JPEG
                _, buffer = cv2.imencode('.jpg', frame)
                # Convert to Base64
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')

                # Publish the Base64-encoded image
                client.publish(IMAGE_TOPIC, jpg_as_text)
                print(f"Captured image and published to '{IMAGE_TOPIC}'")
            else:
                print("Failed to capture image from webcam.")

    except Exception as e:
        print(f"Error in on_message: {e}")

# Create the MQTT client, specifying older callback API (v1) if using Paho 2.x
client = mqtt.Client(client_id="PiCameraNode")

client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker (replace with your broker host if different)
client.connect("raidleypi.local", 1883)

# Blocking network loop
client.loop_forever()
