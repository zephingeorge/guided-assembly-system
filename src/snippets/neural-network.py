# write a program to crop screw images from the camera using the given screw coordinates and then use the model at ../neural-network/model.h5 to predict the presence of the screw

import cv2
import keras
import numpy as np
import tensorflow as tf

print(keras.__version__)
print(tf.__version__)

print("Loading model")
model = keras.models.load_model('./neural-network/model.keras')
print(model.__class__)
print("Model loaded")

# Initialize the video capture
video = cv2.VideoCapture(0)

# Initialize global variables for mouse coordinates
mouseX, mouseY = -1, -1


def predict_image(input_image):
    # Resize the image to 128, 128
    input_image = tf.image.resize(input_image, (128, 128))
    # Call predict on the model
    output = model.predict(np.expand_dims(input_image, axis=0))
    output = output > 0.5
    return output


# Function to calculate cropped frame size and offset
def get_crop_info(frame_shape, click_point, crop_size):
    # Extract frame height and width
    frame_height, frame_width = frame_shape[:2]

    # Calculate half crop size for centering
    half_crop_size = crop_size // 2

    # Ensure click point is within frame boundaries
    click_point_x = max(0, min(click_point[0], frame_width - 1))
    click_point_y = max(0, min(click_point[1], frame_height - 1))

    # Calculate top-left corner coordinates for cropping
    top_left_x = max(0, click_point_x - half_crop_size)
    top_left_y = max(0, click_point_y - half_crop_size)

    # Calculate bottom-right corner coordinates for cropping
    bottom_right_x = min(frame_width, click_point_x + half_crop_size)
    bottom_right_y = min(frame_height, click_point_y + half_crop_size)

    return top_left_x, top_left_y, bottom_right_x, bottom_right_y


# Callback function for handling double-click events
def draw_circle(event, x, y, flags, param):
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        mouseX, mouseY = x, y
        print("Double-clicked at:", mouseX, mouseY)

        # Check if frame is available
        if frame is not None:
            # Define crop size (adjust as needed)
            crop_size = 16

            # Get cropping information
            top_left_x, top_left_y, bottom_right_x, bottom_right_y = get_crop_info(frame.shape, (mouseX, mouseY),
                                                                                   crop_size)

            # Extract cropped frame
            cropped_frame = frame[top_left_y:bottom_right_y, top_left_x:bottom_right_x]

            # Resize cropped frame to 64x64 (adjust interpolation method if needed)
            resized_frame = cv2.resize(cropped_frame, (64, 64), interpolation=cv2.INTER_AREA)
            result = predict_image(resized_frame)
            if result:
                print("------------Screw detected------------")
            else:
                print("-----------No screw detected----------")
            # Define desired filename and path (replace with your preference)
            filename = f"cropped_image_{mouseX}_{mouseY}.jpg"
            filepath = "./neural-network/screw-extracts/" + filename
            print(f"Image : {filepath}")
            cv2.imwrite(filepath, resized_frame)


# Create a window for displaying the image and set up the mouse callback
cv2.namedWindow('Desk Image')
cv2.setMouseCallback('Desk Image', draw_circle)

# Global variable to store the frame (optional for performance)
frame = None

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
