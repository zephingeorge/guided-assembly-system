import cv2
import numpy as np

# Read the image
image = cv2.imread(r"D:\SIT ACAD\SEM 3\Computer Vision\Object Recognition\ScrewHole\white-bg.jpg")

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply edge detection using the Canny filter
edges = cv2.Canny(gray_image, 50, 150)

# Resize the images to be smaller
height, width = image.shape[:2]
resize_factor = 0.5  # You can adjust this factor to make the output smaller or larger
resized_image = cv2.resize(image, (int(width * resize_factor), int(height * resize_factor)))
resized_edges = cv2.resize(edges, (int(width * resize_factor), int(height * resize_factor)))

# Display the resized original and processed images
cv2.imshow('Resized Original Image', resized_image)
cv2.imshow('Resized Edge Detection', resized_edges)
cv2.imwrite(r"D:\SIT ACAD\SEM 3\Computer Vision\Object Recognition\ScrewHole\white-bg-processed.jpg", resized_edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
