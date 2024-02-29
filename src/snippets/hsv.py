import cv2
import numpy as np

def detect_ss_screws(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image from BGR to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the color of SS screws in HSV
    lower_ss_color = np.array([0, 0, 150])
    upper_ss_color = np.array([179, 50, 255])

    # Create a mask to extract only the SS screws based on color
    ss_mask = cv2.inRange(hsv_image, lower_ss_color, upper_ss_color)

    # Apply morphological operations to enhance the mask
    kernel = np.ones((5, 5), np.uint8)
    ss_mask = cv2.morphologyEx(ss_mask, cv2.MORPH_OPEN, kernel)
    ss_mask = cv2.morphologyEx(ss_mask, cv2.MORPH_CLOSE, kernel)

    # Find contours in the mask
    contours, _ = cv2.findContours(ss_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original image
    result_image = image.copy()
    cv2.drawContours(result_image, contours, -1, (0, 255, 0), 2)

    # Display the original and processed images
    cv2.imshow('Original Image', image)
    cv2.imshow('Detected SS Screws', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_path = 'D:\SIT ACAD\SEM 3\Computer Vision\Object Recognition\ScrewHole\photo_2023-12-18_07-40-01.jpg'
detect_ss_screws(image_path)
