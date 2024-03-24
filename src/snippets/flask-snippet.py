from flask import Flask, Response, render_template, request, jsonify
import cv2, time, requests, json
import numpy as np

app = Flask(__name__, static_folder='static', template_folder='templates')

screw_coordinates = []

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/coordinates', methods=['POST'])
def coordinates():
    data = request.get_json()
    screw_coordinates.append(data)

    return jsonify({'status': 'ok'})
@app.route('/')
def index():
    return render_template('index.html')


def generate_frames():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        for screw in screw_coordinates:
            cv2.circle(frame, (int(screw['x']), int(screw['y'])), 5, (0, 0, 255), -1)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
