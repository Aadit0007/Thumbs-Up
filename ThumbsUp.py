import cv2
import mediapipe as mp

# Initialize Mediapipe Hand Detector
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Define a function to detect thumbs up
def is_thumbs_up(hand_landmarks):
    """
    Checks if the detected hand is showing a thumbs-up gesture.
    """
    # Extract landmarks
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

    # Check if the thumb is up while other fingers are closed
    is_thumb_up = thumb_tip.y < thumb_ip.y and thumb_tip.y < index_mcp.y
    is_fingers_down = all(
        hand_landmarks.landmark[finger_tip].y > hand_landmarks.landmark[finger_mcp].y
        for finger_tip, finger_mcp in [
            (mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_MCP),
            (mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_MCP),
            (mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_MCP),
            (mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_MCP),
        ]
    )
    return is_thumb_up and is_fingers_down

# Start capturing video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a mirrored view
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    # Convert frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame
    result = hands.process(rgb_frame)

    # Draw landmarks and check for thumbs up
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Check for thumbs-up gesture
            if is_thumbs_up(hand_landmarks):
                cv2.putText(frame, "👍", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                print("👍")  # Print thumbs-up emoji

    # Display the frame
    cv2.imshow("Thumbs Up Detector", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
