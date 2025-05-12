from psychopy import visual, core, event
from psychopy.iohub import launchHubServer
import cv2

# Launch the iohub server
iohub = launchHubServer()

# Create a window
win = visual.Window(fullscr=True, color=[1, 1, 1])

# Use the default webcam (index 0)
cap = cv2.VideoCapture(0)

# Check if the webcam is accessible
if not cap.isOpened():
    print("Error: Webcam not accessible")
    core.quit()

# Run the eye-tracking loop
while not event.getKeys():
    ret, frame = cap.read()
    if ret:
        # Convert the frame to grayscale (optional, can improve performance)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Display the webcam feed
        cv2.imshow('Eye Tracker', gray_frame)
        
        # Break if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
win.close()
core.quit()
