import cv2
from flask import request, jsonify

from modules.database import read_database, save_database

global screw_coordinates
screw_coordinates = []


def coordinates():
    global screw_coordinates
    data = request.get_json()
    screw_coordinates.append(data)
    return jsonify(len(screw_coordinates))


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


def template_management(frame):
    global screw_coordinates
    for screw in screw_coordinates:
        frame = cv2.circle(frame, (screw[0], screw[1]), 5, (0, 255, 0), 5)
    return frame
