# write a program to crop screw images from the camera using the given screw coordinates and then use the model at ../neural-network/model.h5 to predict the presence of the screw
import time
import cv2
import numpy as np
import keras
import tensorflow as tf
#print keras version
print(keras.__version__)
print(tf.__version__)

cap = cv2.VideoCapture(0)
screw_index = 0
print("Loading model")
# #MOUNT GOOGLE DRIVE
# from google.colab import drive
# drive.mount('/content/drive')
# #load model into keras using file in google drive
model = tf.keras.models.load_model('./image_net_v1_acc_1.h5')




print("Model loaded")

# def predict_image(input_image):
#     # Resize the image to 128, 128
#     input_image = tf.image.resize(input_image, (128, 128))
#     # Call predict on the model
#     output = model.predict(np.expand_dims(input_image, axis=0))
#     output = (output > 0.5).astype(np.float32)
#     return output


screw_coordinates = [
    [270, 235],
    [420, 320],
    [420, 235],
    [270, 320],
]


while True:
    ret, image = cap.read()
    if not ret:
        break
    # if mouse is clicked, crop the image
    # if event == cv2.EVENT_LBUTTONDBLCLK:
    #     # Draw a circle at the double-clicked position
    #     mouseX, mouseY = x, y
    #     x, y = 0, 0
    #     # get the x, y coordinates
    #     x, y = cv2.getMousePosition()
    #     # crop the image for 64x64
    #     crop_img = image[y - 32:y + 32, x - 32:x + 32]
    #     #print shape image
    #     print(crop_img.shape)
    #     # resize the image to 64
    for x, y in screw_coordinates:
        crop_img = image[y - 32:y + 32, x - 32:x + 32]
        resized_image = cv2.resize(crop_img, (64, 64))
        # predict the image
        prediction = predict_image(resized_image)
        screw_coordinates.append({[x, y]: prediction})
    for screw in screw_coordinates:
        for key, value in screw.items():
            x, y = key
            if value:
                cv2.circle(image, (x, y), 5, (0, 255, 0), 2)
            else:
                cv2.circle(image, (x, y), 5, (0, 0, 255), 2)
    cv2.imshow('Video Stream', image)
