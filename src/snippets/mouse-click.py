import cv2
import os

# Set the working directory and filename
os.chdir('C:\\Users\\zephi\\OneDrive\\Pictures')    

# Initialize the video capture
video = cv2.VideoCapture(0)

# Initialize global variables for mouse coordinates
mouseX, mouseY = -1, -1

# Callback function for handling double-click events
def draw_circle(event, x, y, flags, param):
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        # Draw a circle at the double-clicked position
        cv2.circle(frame, (x, y), 100, (255, 0, 0), -1)
        mouseX, mouseY = x, y
        print("Double-clicked at:", mouseX, mouseY)

# Create a window for displaying the image and set up the mouse callback
cv2.namedWindow('Desk Image')
cv2.setMouseCallback('Desk Image', draw_circle)

# Main loop for capturing mouse click coordinates
while True:
    # Read a frame from the video
    check, frame = video.read()

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
