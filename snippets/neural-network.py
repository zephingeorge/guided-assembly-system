# write a program to crop screw images from the camera using the given screw coordinates and then use the model at ../neural-network/model.h5 to predict the presence of the screw

import cv2
import keras
import numpy as np
import tensorflow as tf

print(keras.__version__)
print(tf.__version__)

print("Loading model")
model = keras.models.load_model('../neural-network/model.keras')
print(model.__class__)
print("Model loaded")

# Initialize the video capture
video = cv2.VideoCapture(1)

# Initialize global variables for mouse coordinates
mouseX, mouseY = -1, -1


# Callback function for handling double-click events
def draw_circle(event, x, y, flags, param):
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        mouseX, mouseY = x, y
        print("Double-clicked at:", mouseX, mouseY)

        # Check if frame is available
        if frame is not None:
            # Define crop size (adjust as needed)
            crop_size = 20
            frame_height, frame_width, _ = frame.shape
            half_crop_size = crop_size // 2
            click_point_x = max(0, min(x, frame_width - 1))
            click_point_y = max(0, min(y, frame_height - 1))
            top_left_x = max(0, click_point_x - half_crop_size)
            top_left_y = max(0, click_point_y - half_crop_size)
            bottom_right_x = min(frame_width, click_point_x + half_crop_size)
            bottom_right_y = min(frame_height, click_point_y + half_crop_size)
            cropped_frame = frame[top_left_y:bottom_right_y, top_left_x:bottom_right_x]
            cropped_frame_rgb = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2RGB)
            resized_frame = cv2.resize(cropped_frame_rgb, (64, 64), interpolation=cv2.INTER_AREA)
            screw_patch = tf.image.resize(resized_frame, (128, 128))
            prediction = model.predict(np.expand_dims(screw_patch, axis=0))
            print('prediction: ', prediction)
            predicted_class = np.argmax(prediction, axis=1)
            print('predicted class: ', predicted_class)
            if predicted_class[0] == 0:
                print("m4")
            elif predicted_class[0] == 1:
                print("m8")
            elif predicted_class[0] == 2:
                print("m12")
            elif predicted_class[0] == 3:
                print("none")
            else:
                print("unknown")
            filename = f"cropped_image_{mouseX}_{mouseY}.jpg"
            filepath = "../neural-network/screw-extracts/" + filename
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
