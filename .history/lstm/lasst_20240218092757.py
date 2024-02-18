import cv2
import numpy as np
from tensorflow.keras.models import load_model
from mediapipe import mediapipe_detection, draw_styled_landmarks, extract_keypoints

# Load the trained model
model = load_model('action.h5')

# Define the actions
actions = ['hello', 'thanks', 'iloveyou']

# Define colors for visualization
colors = [(245,117,16), (117,245,16), (16,117,245)]

# Define a function to visualize probabilities
def prob_viz(res, actions, input_frame, colors):
    output_frame = input_frame.copy()
    for num, prob in enumerate(res):
        cv2.rectangle(output_frame, (0,60+num*40), (int(prob*100), 90+num*40), colors[num], -1)
        cv2.putText(output_frame, actions[num], (0, 85+num*40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
    return output_frame

# Set mediapipe model
mp_holistic = mp.solutions.holistic

# Open the webcam
cap = cv2.VideoCapture(0)

# Initialize variables for gesture recognition
sequence = []
sentence = []
predictions = []
threshold = 0.5

# Loop through video frames
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Make detections
        image, results = mediapipe_detection(frame, holistic)
        
        # Draw landmarks
        draw_styled_landmarks(image, results)
        
        # Perform gesture recognition
        keypoints = extract_keypoints(results)
        sequence.append(keypoints)
        sequence = sequence[-30:]  # Keep only the last 30 frames
        
        # Make prediction every 30 frames
        if len(sequence) == 30:
            res = model.predict(np.expand_dims(sequence, axis=0))[0]
            predictions.append(np.argmax(res))
            
            # Update sentence based on predictions
            if np.unique(predictions[-10:])[0] == np.argmax(res) and res[np.argmax(res)] > threshold:
                sentence.append(actions[np.argmax(res)])
                if len(sentence) > 5:
                    sentence = sentence[-5:]
            
            # Visualize probabilities
            image = prob_viz(res, actions, image, colors)
        
        # Display sentence on the screen
        cv2.rectangle(image, (0,0), (640, 40), (245, 117, 16), -1)
        cv2.putText(image, ' '.join(sentence), (3,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Show the frame
        cv2.imshow('Gesture Recognition', image)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
