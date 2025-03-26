#%% Reference: https://github.com/googlesamples/mediapipe/tree/main/examples/hand_landmarker/raspberry_pi
# Download hand land mark detector model wget -q https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

#%% Parameters
numHands = 2  # Number of hands to be detected
model = 'hand_landmarker.task'  # Model for finding the hand landmarks
minHandDetectionConfidence = 0.5  # Thresholds for detecting the hand
minHandPresenceConfidence = 0.5
minTrackingConfidence = 0.5
frameWidth = 640
frameHeight = 480

# Visualization parameters
MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54)  # vibrant green
LANDMARK_COLOR = (0, 255, 0)  # Green for landmarks
LINE_COLOR = (255, 0, 0)  # Blue for skeleton lines

# Mediapipe hand connections for drawing skeleton
mp_hands = mp.solutions.hands
HAND_CONNECTIONS = mp_hands.HAND_CONNECTIONS  # Connections between landmarks

#%% Create a HandLandmarker object.
base_options = python.BaseOptions(model_asset_path=model)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=numHands,
    min_hand_detection_confidence=minHandDetectionConfidence,
    min_hand_presence_confidence=minHandPresenceConfidence,
    min_tracking_confidence=minTrackingConfidence)
detector = vision.HandLandmarker.create_from_options(options)

#%% Open CV Video Capture and frame analysis
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# The loop will break on pressing the 'q' key
while True:
    try:
        # Capture one frame
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)  # Flip image to match camera view

        # Convert the image from BGR to RGB as required by Mediapipe model
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Run hand landmarker using the model.
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        detection_result = detector.detect(mp_image)

        hand_landmarks_list = detection_result.hand_landmarks

        # Loop through the detected hands to visualize.
        for hand_landmarks in hand_landmarks_list:
            landmark_points = []

            # Draw all 21 landmarks
            for idx, landmark in enumerate(hand_landmarks):
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                landmark_points.append((x, y))

                # Draw landmark points
                cv2.circle(frame, (x, y), 5, LANDMARK_COLOR, -1)

            # Draw skeleton lines using HAND_CONNECTIONS
            for connection in HAND_CONNECTIONS:
                start_idx, end_idx = connection
                if start_idx < len(landmark_points) and end_idx < len(landmark_points):
                    cv2.line(frame, landmark_points[start_idx], landmark_points[end_idx], LINE_COLOR, 2)

        # Show the annotated frame
        cv2.imshow('Hand Landmark Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except KeyboardInterrupt:
        break

cap.release()
cv2.destroyAllWindows()
