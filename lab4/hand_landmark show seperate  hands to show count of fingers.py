import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

#%% Parameters
numHands = 2  # Detect up to 2 hands
model = 'hand_landmarker.task'  
minHandDetectionConfidence = 0.5  
minHandPresenceConfidence = 0.5
minTrackingConfidence = 0.5
frameWidth = 640
frameHeight = 480

# Colors for visualization
MARGIN = 10
FONT_SIZE = 1
FONT_THICKNESS = 2
TEXT_COLOR = (255, 255, 255)  # White
LANDMARK_COLOR = (0, 255, 0)  # Green
LINE_COLOR = (255, 0, 0)  # Blue

# Mediapipe hand connections for drawing skeleton
mp_hands = mp.solutions.hands
HAND_CONNECTIONS = mp_hands.HAND_CONNECTIONS  

#%% Create a HandLandmarker object
base_options = python.BaseOptions(model_asset_path=model)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=numHands,
    min_hand_detection_confidence=minHandDetectionConfidence,
    min_hand_presence_confidence=minHandPresenceConfidence,
    min_tracking_confidence=minTrackingConfidence)
detector = vision.HandLandmarker.create_from_options(options)

#%% Open CV Video Capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# The loop will break on pressing 'q'
while True:
    try:
        # Capture one frame
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)  # Flip image to match mirror view

        # Convert the image from BGR to RGB as required by Mediapipe
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Run hand detection
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        detection_result = detector.detect(mp_image)

        hand_landmarks_list = detection_result.hand_landmarks
        total_fingers = 0  # Store the total number of fingers raised

        # Process each detected hand
        for hand_landmarks in hand_landmarks_list:
            landmark_points = []
            
            # Convert landmarks to pixel coordinates
            for idx, landmark in enumerate(hand_landmarks):
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                landmark_points.append((x, y))

                # Draw landmark points
                cv2.circle(frame, (x, y), 5, LANDMARK_COLOR, -1)

            # Draw skeleton lines
            for connection in HAND_CONNECTIONS:
                start_idx, end_idx = connection
                if start_idx < len(landmark_points) and end_idx < len(landmark_points):
                    cv2.line(frame, landmark_points[start_idx], landmark_points[end_idx], LINE_COLOR, 2)

            # **FINGER COUNTING LOGIC**
            fingers = 0

            # Thumb (Check if it's raised)
            thumb_tip = hand_landmarks[4]
            thumb_base = hand_landmarks[2]
            index_finger = hand_landmarks[8]

            if thumb_tip.x < thumb_base.x:  # Thumb is open if it's left of base for right hand
                fingers += 1

            # Other fingers (index, middle, ring, pinky)
            finger_tips = [8, 12, 16, 20]  # Indices for the tips
            finger_pips = [6, 10, 14, 18]  # Indices for the PIP joints

            for tip, pip in zip(finger_tips, finger_pips):
                if hand_landmarks[tip].y < hand_landmarks[pip].y:  # Tip is higher than PIP
                    fingers += 1

            total_fingers += fingers

        # Display total fingers count on the image
        cv2.putText(frame, f'Fingers: {total_fingers}', (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, FONT_SIZE, TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

        # Show the frame
        cv2.imshow('Hand Landmark Detection & Finger Counting', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except KeyboardInterrupt:
        break

cap.release()
cv2.destroyAllWindows()
