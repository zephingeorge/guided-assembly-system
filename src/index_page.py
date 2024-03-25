import time

import cv2
import numpy as np
from flask import jsonify, request

from modules.database import read_database
from modules.neural_network import verify_screw_presence
from pupil_apriltags import Detector

screw_coordinates = []
screwdriver_tag_id = 3


def template_list_details():
    details = []
    templates_list = read_database()
    for template_id in templates_list:
        details.append({'id': template_id, 'name': templates_list[template_id]['name']})
    return jsonify(details)


def get_template():
    global screw_coordinates
    data = request.get_json()
    template_id = data['id']
    templates_list = read_database()
    screw_coordinates = templates_list[str(template_id)]['screws']
    return jsonify(templates_list[template_id])


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
    at_detector = Detector(
        families='tag36h11',
        nthreads=1,
        quad_decimate=1.0,
        quad_sigma=0.0,
        refine_edges=1,
        decode_sharpening=0.25,
        debug=0
    )
    # Process image:
    # 1. Convert to grayscale
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 2. Detect AprilTags
    tags = at_detector.detect(gray_image)
    #
    # # 3. Analyze screwdriver and screws
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
        print("Screwing screw ", screw_index + 1)
        # check if the screwdriver is close enough to the screw
        print("Distance to screw ", screwdriver_to_screw[nearest_screw])
        if screwdriver_to_screw[nearest_screw] < 30:

            # draw an orange circle on the screw to indicate screwing
            frame = cv2.circle(frame, (screw_coordinates[nearest_screw][0], screw_coordinates[nearest_screw][1]),
                               radius=8, color=(0, 165, 255), thickness=8)
            # check if start_time has been initialized
            if 'start_time' not in locals():
                print("start_time initialized")
                start_time = time.time()
            else:
                print("Elapsed time ", time.time() - start_time)
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
                    # ask to move screwdriver away
                    cv2.putText(frame, "Move screwdriver away", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                (0, 255, 0), 2, cv2.LINE_AA)
                    if screwdriver_to_screw[nearest_screw] > 200:
                        for index, screw in enumerate(screw_coordinates):
                            # check if screw is present using neural network
                            status = verify_screw_presence(frame, screw[0], screw[1])
                            if status:
                                print(index + 1, " Screw ", screw, " is present")
                            else:
                                print(index + 1, " Screw ", screw, " is missing")
                                break
                        print("All screws have been screwed")
                    cv2.putText(frame, "All screws have been screwed", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                (0, 255, 0), 2, cv2.LINE_AA)
                    return
    # display green circle on screws that have been screwed
    for i in range(screw_index):
        frame = cv2.circle(frame, (screw_coordinates[i][0], screw_coordinates[i][1]), 8,
                           (0, 255, 0), 8)
    return frame
