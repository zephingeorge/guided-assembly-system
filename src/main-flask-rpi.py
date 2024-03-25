import apriltag
import time

import numpy as np
from flask import Flask, render_template, jsonify, request

from src.modules.camera import *
from src.modules.database import save_database, read_database

application_mode = "screwing"
screw_coordinates = []
screwdriver_tag_id = 3

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/template_list_details', methods=['GET'], endpoint='template_list_details')
def template_list_details():
    details = []
    templates_list = read_database()
    for template_id in templates_list:
        details.append({'id': template_id, 'name': templates_list[template_id]['name']})
    return jsonify(details)


@app.route('/get_template', methods=['POST'], endpoint='get_template')
def get_template():
    global screw_coordinates
    data = request.get_json()
    template_id = data['id']
    templates_list = read_database()
    screw_coordinates = templates_list[str(template_id)]['screws']
    return jsonify(templates_list[template_id])


@app.route('/coordinates', methods=['POST'], endpoint='coordinates')
def coordinates():
    global screw_coordinates
    data = request.get_json()
    screw_coordinates.append(data)
    return jsonify(len(screw_coordinates))


@app.route('/save_template', methods=['POST'], endpoint='save_template')
def save_template():
    global screw_coordinates
    if len(screw_coordinates) == 0:
        return jsonify({'status': 'error', 'message': 'No screws sequence found'})
    data = request.get_json()
    data['screws'] = screw_coordinates
    templates_list = read_database()
    templates_list[str(len(templates_list))] = data
    save_database(templates_list)
    screw_coordinates.clear()
    return jsonify({'status': 'success', 'message': 'Template saved successfully'})


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# template page
@app.route('/templates', methods=['GET'], endpoint='templates')
def templates():
    global application_mode, screw_coordinates
    screw_coordinates = []
    application_mode = "template_management"
    return render_template('templates.html')


# switch to home page
@app.route('/')
def index():
    global application_mode, screw_coordinates
    screw_coordinates = []
    application_mode = "screwing"
    return render_template('index.html')


def template_management(frame):
    global screw_coordinates
    for screw in screw_coordinates:
        frame = cv2.circle(frame, (screw[0], screw[1]), 5, (0, 255, 0), 5)
    return frame


def generate_frames():
    camera_object = start_camera(640, 480)
    while True:
        frame = get_camera_frame(camera_object)
        if application_mode == "screwing":
            frame = screwing_process(frame)
        elif application_mode == "template_management":
            frame = template_management(frame)
        else:
            break
        yield prepare_frame_for_stream(frame)
    stop_camera(camera_object)


def screwing_process(frame):
    global screw_coordinates, screwdriver_tag_id
    if not screw_coordinates:
        # Display message that no template has been selected
        cv2.putText(frame, "Template Error, No Screws Sequence Found", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 255, 0), 2, cv2.LINE_AA)
        return frame
    screwdriver_center = np.array([0, 0])
    screw_index = 0
    start_time = 0
    at_detector = apriltag.Detector()
    # Process image:
    # 1. Convert to grayscale
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 2. Detect AprilTags
    tags = at_detector.detect(gray_image)

    # 3. Analyze screwdriver and screws
    for tag in tags:
        if tag.tag_id == screwdriver_tag_id:
            screwdriver_center = tag.center
            screwdriver_center = (int(screwdriver_center[0]), int(screwdriver_center[1]))
            break

    screwdriver_to_screw = []
    for position in screw_coordinates:
        distance = np.linalg.norm(screwdriver_center - np.array([position[0], position[1]]))
        screwdriver_to_screw.append(distance)
        cv2.circle(frame, (position[0], position[1]), 5, (0, 255, 0), 5)
    nearest_screw = np.argmin(screwdriver_to_screw)

    # 4. Display information and circles
    cv2.putText(frame, "Next Screw : " + str(screw_index + 1), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (0, 255, 0), 2, cv2.LINE_AA)
    frame = cv2.circle(frame, (screw_coordinates[screw_index][0], screw_coordinates[screw_index][1]), 8,
                       (0, 255, 0), 2)
    cv2.circle(frame, screwdriver_center, 5, (0, 0, 255), 2)
    cv2.putText(frame, "Nearest Screw : " + str(nearest_screw + 1), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (0, 255, 0), 2, cv2.LINE_AA)
    frame = cv2.circle(frame, (screw_coordinates[nearest_screw][0], screw_coordinates[nearest_screw][1]), 5,
                       (0, 0, 255), 5)

    # Draw a circle at the nearest screw
    frame = cv2.circle(frame, (screw_coordinates[nearest_screw][0], screw_coordinates[nearest_screw][1]), radius=0,
                       color=(0, 0, 255), thickness=5)

    # check if the nearest screw is the next screw to be screwed
    if nearest_screw == screw_index:
        # check if the screwdriver is close enough to the screw
        if screwdriver_to_screw[nearest_screw] < 30:
            # draw an orange circle on the screw to indicate screwing
            frame = cv2.circle(frame, (screw_coordinates[nearest_screw][0], screw_coordinates[nearest_screw][1]),
                               radius=8, color=(0, 165, 255), thickness=8)
            # check if start_time has been initialized
            if 'start_time' not in locals():
                start_time = time.time()
            else:
                elapsed_time = time.time() - start_time
                # check if the screw has been screwed for 2 seconds
                if elapsed_time > 2:
                    # delete start_time
                    del start_time
                    # increment screw_index
                    screw_index += 1
                    # check if all screws have been screwed
                if screw_index == len(screw_coordinates):
                    # break the loop and display message that all screws have been screwed
                    print("All screws have been screwed")
                    cv2.putText(frame, "All screws have been screwed", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                (0, 255, 0), 2, cv2.LINE_AA)
                    return
    # display green circle on screws that have been screwed
    for i in range(screw_index):
        frame = cv2.circle(frame, (screw_coordinates[i][0], screw_coordinates[i][1]), 8,
                           (0, 255, 0), 8)
    return frame


app.run(host='0.0.0.0', debug=True)
