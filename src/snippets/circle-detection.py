import cv2
import numpy as np

def detect_objects_live():
    # Open a connection to the camera (0 represents the default camera, you can change it if needed)
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the video stream
        ret, frame = cap.read()
        if not ret:
            print("Error reading frame")
            
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply GaussianBlur to reduce noise and help object detection
        blurred = cv2.GaussianBlur(gray, (15, 15), 0)

        # Use HoughCircles to detect circles in the frame
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT, 
            dp=1,
            minDist=10,
            param1=50,
            param2=35,
            minRadius=1,
            maxRadius=80
        )
99
        # If circles are found, draw them on the frame
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # Draw the outer circle
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # Draw the center of the circle
                cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)

        # Display the result
        cv2.imshow('Object Detection', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Example usage for live video stream
detect_objects_live()
