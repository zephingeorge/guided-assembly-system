import cv2
import numpy as np

def detect_ss_screws_edge(image_path, filter_type='sobel'):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Sobel or Prewitt filter for edge detection
    if filter_type == 'sobel':
        edges = cv2.Sobel(gray_image, cv2.CV_64F, 1, 1, ksize=3)
    elif filter_type == 'prewitt':
        kernel_x = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
        kernel_y = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        edges_x = cv2.filter2D(gray_image, -1, kernel_x)
        edges_y = cv2.filter2D(gray_image, -1, kernel_y)
        edges = edges_x + edges_y
    else:
        raise ValueError("Invalid filter type. Choose 'sobel' or 'prewitt'.")

    # Threshold the edges to create a binary mask
    _, binary_mask = cv2.threshold(np.abs(edges).astype(np.uint8), 50, 255, cv2.THRESH_BINARY)

    # Apply morphological operations to enhance the mask
    kernel = np.ones((5, 5), np.uint8)
    binary_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_OPEN, kernel)
    binary_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel)

    # Find contours in the mask
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original image
    result_image = image.copy()
    cv2.drawContours(result_image, contours, -1, (0, 255, 0), 2)

    # Display the original and processed images
    cv2.imshow('Original Image', image)
    cv2.imshow(f'Detected SS Screws ({filter_type.capitalize()} Filter)', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_path = "D:\SIT ACAD\SEM 3\Computer Vision\Object Recognition\ScrewHole\photo_2023-12-18_07-40-01.jpg"
detect_ss_screws_edge(image_path, filter_type='sobel')
