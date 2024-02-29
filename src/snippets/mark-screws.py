import cv2
import os

# Set the working directory and filename
os.chdir('C:\\Users\\zephi\\OneDrive\\Pictures')    

# Initialize the video capture
video = cv2.VideoCapture(0)

# Define screw coordinates
screw_coordinates = [
    [270, 235],
    [270, 320],
    [420, 235],
    [420, 320]
]

# Main loop for drawing circles at predefined screw coordinates
while True:
    # Read a frame from the video
    check, frame = video.read()

    # Draw circles at predefined screw coordinates
    for position in screw_coordinates:
        frame = cv2.circle(frame, (position[0], position[1]), radius=0, color=(0, 0, 0), thickness=8)

    # Display the frame in the 'Desk Image' window
    cv2.imshow('Desk Image', frame)

    # Check for key events
    key = cv2.waitKey(1)
    # Break the loop on 'Esc' key or 'q' key
    if key == 27 or key == ord('q'):  
        break

# Release the video capture and close all windows
video.release()
cv2.destroyAllWindows()
