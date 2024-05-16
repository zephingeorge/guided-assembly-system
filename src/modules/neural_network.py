import cv2
import keras
import numpy as np
import tensorflow as tf
import time

model = keras.models.load_model('../neural-network/model.keras')


def verify_screw_presence(input_frame, x, y):
    crop_size = 20
    frame_height, frame_width, _ = input_frame.shape
    half_crop_size = crop_size // 2
    click_point_x = max(0, min(x, frame_width - 1))
    click_point_y = max(0, min(y, frame_height - 1))
    top_left_x = max(0, click_point_x - half_crop_size)
    top_left_y = max(0, click_point_y - half_crop_size)
    bottom_right_x = min(frame_width, click_point_x + half_crop_size)
    bottom_right_y = min(frame_height, click_point_y + half_crop_size)
    cropped_frame = input_frame[top_left_y:bottom_right_y, top_left_x:bottom_right_x]
    cropped_frame_rgb = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2RGB)
    resized_frame = cv2.resize(cropped_frame_rgb, (64, 64), interpolation=cv2.INTER_AREA)
    screw_patch = tf.image.resize(resized_frame, (128, 128))
    filename = f"cropped_image_date_{time.time()}.jpg"
    filepath = "./neural-network/screw-extracts/" + filename
    print(f"Image : {filepath}")
    cv2.imwrite(filepath, resized_frame)
    prediction = model.predict(np.expand_dims(screw_patch, axis=0))
    predicted_class = np.argmax(prediction, axis=1)
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
