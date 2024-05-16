import cv2
from flask import Response


def start_camera(height=0, width=0):
    camera_object = cv2.VideoCapture(0)
    if height == 0 or width == 0:
        ret, frame = camera_object.read()
        return camera_object
    camera_object.set(3, width)
    camera_object.set(4, height)
    ret, frame = camera_object.read()
    return camera_object


def get_camera_frame(camera_object):
    ret, frame = camera_object.read()
    if not ret:
        return
    return frame


def stop_camera(camera_object):
    camera_object.release()


def prepare_frame_for_stream(frame):
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    return b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
