from flask import Flask, Response, render_template, request
import cv2, time
import numpy as np
from pupil_apriltags import Detector

app = Flask(__name__)

# Define constants
screwdriver_tagid = 3
screw_coordinates = [
    [270, 235], [420, 320], [420, 235], [270, 320]
]

# Flag to control video streaming
is_streaming = True


def generate_frames():
    cap = cv2.VideoCapture(0)

    # Detector and initialization
    at_detector = Detector(
        families='tag36h11',
        nthreads=1,
        quad_decimate=2.0,
        quad_sigma=0.0,
        refine_edges=1,
        decode_sharpening=0.25,
        debug=0,
    )

    screwdriver_center = np.array([0, 0])
    screw_index = 0
    start_time = None

    while True:
        if not is_streaming:
            # Pause streaming when the flag is False
            continue

        ret, image = cap.read()
        if not ret:
            break

        # Process image:
        # 1. Convert to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 2. Detect AprilTags
        tags = at_detector.detect(gray_image, estimate_tag_pose=False, camera_params=None, tag_size=None)

        # 3. Analyze screwdriver and screws
        for tag in tags:
            if tag.tag_id == screwdriver_tagid:
                screwdriver_center = tag.center
                screwdriver_center = (int(screwdriver_center[0]), int(screwdriver_center[1]))
                break

        screwdriver_to_screw = []
        for index, position in enumerate(screw_coordinates):
            x, y = position
            screw_center = np.array([x, y])
            distance = np.linalg.norm(screwdriver_center - screw_center)
            screwdriver_to_screw.append(distance)

        nearest_screw = np.argmin(screwdriver_to_screw)

        # 4. Display information and circles
        cv2.putText(image, "Next Screw : " + str(screw_index + 1), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 255, 0), 2, cv2.LINE_AA)
        image = cv2.circle(image, (screw_coordinates[screw_index][0], screw_coordinates[screw_index][1]), 8,
                           (0, 255, 0), 2)
        cv2.circle(image, screwdriver_center, 5, (0, 0, 255), 2)
        cv2.putText(image, "Nearest Screw : " + str(nearest_screw + 1), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 255, 0), 2, cv2.LINE_AA)
        image = cv2.circle(image, (screw_coordinates[nearest_screw][0], screw_coordinates[nearest_screw][1]), 5,
                           (0, 0, 255), 5)

        # Draw a circle at the nearest screw
        frame = cv2.circle(frame, (screw_coordinates[nearest_screw][0], screw_coordinates[nearest_screw][1]), radius=0,
                           color=(0, 0, 255), thickness=5)

        # check if the nearest screw is the next screw to be screwed
        if nearest_screw == screw_index:
            # check if the screwdriver is close enough to the screw
            if screwdriver_to_screw[nearest_screw] < 30:
                # draw a orange circle on the screw to indicate screwing
                frame = cv2.circle(frame, (screw_coordinates[nearest_screw][0], screw_coordinates[nearest_screw][1]),
                                   radius=8, color=(0, 165, 255), thickness=8)
                # check if start_time has been initialized
                if 'start_time' not in locals():
                    start_time = time.time()
                else:
                    elapsed_time = time.time() - start_time
                    # check if the screw has been screwed for 2 seconds
                    if elapsed_time > 2:
                        # deinitialize start_time
                        del start_time
                        # increment screw_index
                        screw_index += 1
                        # check if all screws have been screwed
                        if screw_index == len(screw_coordinates):
                            # break the loop and display message that all screws have been screwed
                            print("All screws have been screwed")
                            cv2.putText(frame, "All screws have been screwed", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                        (0, 255, 0), 2, cv2.LINE_AA)
                            break
        # display green circle on screws that have been screwed
        for i in range(screw_index):
            frame = cv2.circle(frame, (screw_coordinates[i][0], screw_coordinates[i][1]), 8,
                               (0, 255, 0), 8)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        # Check for key events (optional, if needed)
        # key = cv2.waitKey(1)
        # if key == 27 or key == ord('q'):
        #     break

    cap.release()


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
