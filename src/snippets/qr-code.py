import cv2
import os
import numpy as np

# Set the working directory and filename
os.chdir('C:\\Users\\zephi\\OneDrive\\Pictures')    
         
# Initialize the video capture
video = cv2.VideoCapture(0)

# Initialize a QR code detector
qrDecoder = cv2.QRCodeDetector()

# Main loop for QR code detection
while True:
    # Read a frame from the video
    check, frame = video.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect QR code in the frame
    data, bbox, rectifiedImage = qrDecoder.detectAndDecode(frame)

    # If QR code is detected, process it
    if len(data) > 0:
        bbox = bbox.astype(int)
        # Draw a rectangle around the detected QR code
        cv2.rectangle(frame, bbox[0][0], bbox[0][2], (255, 0, 0), 2)
        # Calculate and display the position of the screwdriver
        bounding_box = np.array(bbox)
        vertices = bounding_box[0]
        x_coordinates = vertices[:, 0]
        y_coordinates = vertices[:, 1]
        center_x = np.mean(x_coordinates)
        center_y = np.mean(y_coordinates)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,
                    "Position of the Screw Driver:" + str(center_x) + "" + str(center_y),
                    (10, 450), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        print("Position of the Screw Driver:", int(center_x), int(center_y))
        # Draw a circle at the calculated position
        frame = cv2.circle(frame, (int(center_x), int(center_y)), radius=0, color=(0, 0, 0), thickness=4)

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
