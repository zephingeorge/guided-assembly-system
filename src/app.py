# import apriltag

from flask import Flask, render_template

import index_page
import template_page
from modules.camera import *

application_mode = "screwing"

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/template_list_details', methods=['GET'])
def template_list_details():
    return index_page.template_list_details()


@app.route('/get_template', methods=['POST'])
def get_template():
    return index_page.get_template()


@app.route('/coordinates', methods=['POST'], endpoint='coordinates')
def coordinates():
    return template_page.coordinates()


@app.route('/save_template', methods=['POST'], endpoint='save_template')
def save_template():
    return template_page.save_template()

@app.route('/clear_screws', methods=['POST'], endpoint='clear_screws')
def clear_screws():
    return template_page.clear_screws()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# template page
@app.route('/templates', methods=['GET'], endpoint='templates')
def templates():
    global application_mode
    application_mode = "templates"
    return render_template('templates.html')


# switch to home page
@app.route('/')
def index():
    global application_mode
    application_mode = "screwing"
    return render_template('index.html')


def generate_frames():
    camera_object = start_camera(0, 0) #640,480
    while True:
        frame = get_camera_frame(camera_object)
        if frame is None:
            break
        if application_mode == "screwing":
            frame = index_page.screwing_process(frame)
        elif application_mode == "templates":
            frame = template_page.template_management(frame)
        else:
            print("Invalid Application Mode")
            break
        yield prepare_frame_for_stream(frame)
    stop_camera(camera_object)


app.run(host='0.0.0.0', debug=True)
