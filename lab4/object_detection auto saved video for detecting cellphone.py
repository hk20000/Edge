import cv2
import mediapipe as mp
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

#%% Parameters
maxResults = 5
scoreThreshold = 0.25
frameWidth = 640
frameHeight = 480
model = 'efficientdet.tflite'
save_video = True  # Set to True to save the summarized video

# Object category to filter (e.g., "cell phone")
TARGET_OBJECT = "cell phone"

# Video output settings
output_filename = "summarized_video.mp4"
fps = 20  # Frames per second for the output video
frame_size = (frameWidth, frameHeight)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for saving video
out = cv2.VideoWriter(output_filename, fourcc, fps, frame_size)

# Visualization parameters
MARGIN = 10
ROW_SIZE = 30
FONT_SIZE = 1
FONT_THICKNESS = 1
TEXT_COLOR = (0, 0, 0)

#%% Initializing results
detection_frame = None
detection_result_list = []

def save_result(result: vision.ObjectDetectorResult, unused_output_image: mp.Image, timestamp_ms: int):
    """Callback function to store the detection results."""
    detection_result_list.append(result)

#%% Create an object detector
base_options = python.BaseOptions(model_asset_path=model)
options = vision.ObjectDetectorOptions(base_options=base_options,
                                       running_mode=vision.RunningMode.LIVE_STREAM,
                                       max_results=maxResults, score_threshold=scoreThreshold,
                                       result_callback=save_result)
detector = vision.ObjectDetector.create_from_options(options)

#%% OpenCV Video Capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

# Loop for real-time processing
while True:
    try:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)  # Mirror the image

        # Convert frame to RGB for Mediapipe processing
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        current_frame = frame.copy()

        # Run object detection asynchronously
        detector.detect_async(mp_image, time.time_ns() // 1_000_000)

        detected_objects = []  # Store detected object names

        if detection_result_list:
            for detection in detection_result_list[0].detections:
                # Extract bounding box
                bbox = detection.bounding_box
                start_point = bbox.origin_x, bbox.origin_y
                end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height

                # Draw bounding box
                cv2.rectangle(current_frame, start_point, end_point, (0, 165, 255), 3)

                # Get detected category and confidence score
                category = detection.categories[0]
                category_name = category.category_name.lower()
                probability = round(category.score, 2)
                result_text = f"{category_name} ({probability})"
                text_location = (MARGIN + bbox.origin_x, MARGIN + ROW_SIZE + bbox.origin_y)

                cv2.putText(current_frame, result_text, text_location, cv2.FONT_HERSHEY_DUPLEX,
                            FONT_SIZE, TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

                detected_objects.append(category_name)

            # If the target object is found, save the frame to the summarized video
            if TARGET_OBJECT in detected_objects:
                print(f"Saving frame with {TARGET_OBJECT} detected.")
                out.write(current_frame)  # Save frame to video file

            detection_frame = current_frame
            detection_result_list.clear()

        # Show the video feed
        if detection_frame is not None:
            cv2.imshow('Object Detection & Summarization', detection_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except KeyboardInterrupt:
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
