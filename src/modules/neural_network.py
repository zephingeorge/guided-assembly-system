import cv2
import keras
import numpy as np
import tensorflow as tf

model = keras.models.load_model('../neural-network/model.keras')


def verify_screw_presence(input_frame, x, y):
    frame_shape = input_frame.shape
    crop_size = 16
    frame_height, frame_width = frame_shape[:2]
    half_crop_size = crop_size // 2
    click_point_x = max(0, min(x, frame_width - 1))
    click_point_y = max(0, min(y, frame_height - 1))
    top_left_x = max(0, click_point_x - half_crop_size)
    top_left_y = max(0, click_point_y - half_crop_size)
    bottom_right_x = min(frame_width, click_point_x + half_crop_size)
    bottom_right_y = min(frame_height, click_point_y + half_crop_size)
    cropped_frame = input_frame[top_left_y:bottom_right_y, top_left_x:bottom_right_x]
    cropped_frame = cv2.resize(cropped_frame, (64, 64), interpolation=cv2.INTER_AREA)
    resized_image = tf.image.resize(cropped_frame, (128, 128))
    prediction = model.predict(resized_image)
    print('prediction: ', prediction)
    predicted_class = np.argmax(prediction, axis=1)
    print('predicted class: ', predicted_class)
    if predicted_class[0] == 0:
        return "m4"
    elif predicted_class[0] == 1:
        return "m8"
    elif predicted_class[0] == 2:
        return "m12"
    elif predicted_class[0] == 3:
        return "none"
    else:
        return "unknown"
