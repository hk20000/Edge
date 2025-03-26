import paho.mqtt.client as mqtt
import base64
import cv2
import numpy as np
import time

# Topics
REQUEST_TOPIC = "camera/request"
IMAGE_TOPIC = "camera/image"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Laptop Node connected to MQTT broker.")
        # Subscribe to the topic where the image is published
        client.subscribe(IMAGE_TOPIC)
        print(f"Subscribed to '{IMAGE_TOPIC}'")
    else:
        print(f"Failed to connect. Return code: {rc}")

def on_message(client, userdata, msg):
    try:
        # The incoming message is a Base64-encoded JPEG
        jpg_as_text = msg.payload.decode('utf-8')
        print(f"Received image data on '{msg.topic}'")

        # Decode from Base64 to bytes
        jpg_original = base64.b64decode(jpg_as_text)

        # Convert bytes to a NumPy array, then decode to an OpenCV image
        np_arr = np.frombuffer(jpg_original, dtype=np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # (Optional) Display the image in a window - comment out if not desired
        # cv2.imshow("Received Image", img)
        # cv2.waitKey(500)  # Display for 0.5 second (requires GUI environment)

        # Save to disk
        filename = "captured.jpg"
        cv2.imwrite(filename, img)
        print(f"Saved image to {filename}")

    except Exception as e:
        print(f"Error handling image data: {e}")

# Create the MQTT client, specifying older callback API (v1) for Paho 2.x
client = mqtt.Client(client_id="LaptopNode")
client.on_connect = on_connect
client.on_message = on_message

# Connect to the same broker
client.connect("raidleypi.local", 1883)
client.loop_start()

# Publish capture requests periodically or on demand
try:
    while True:
        # Send a "capture" request to the Pi
        client.publish(REQUEST_TOPIC, "capture")
        print(f"Published capture request to '{REQUEST_TOPIC}'")
        time.sleep(10)  # Wait before requesting another capture

except KeyboardInterrupt:
    print("Stopping the laptop node...")
finally:
    client.loop_stop()
    client.disconnect()
