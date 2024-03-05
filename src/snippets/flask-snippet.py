from flask import Flask, Response, render_template, request
import cv2

app = Flask(__name__)

# Flag to control video streaming
is_streaming = True

def generate_frames():
    cap = cv2.VideoCapture(0)  # Replace 0 with video source index if needed

    while True:
        if not is_streaming:
            # Pause streaming when the flag is False
            continue

        ret, frame = cap.read()
        if not ret:
            break

        # Process frame here (optional)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
