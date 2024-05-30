import time

import cv2
import numpy as np
from flask import jsonify, request

from modules.database import read_database
from modules.neural_network import verify_screw_presence
import apriltag

screw_coordinates = []
screwdriver_tag_id = 3
start_time = 0
screw_index = 0
wait_time = 0
results = []


def template_list_details():
    details = []
    templates_list = read_database()
    for template_id in templates_list:
        details.append({'id': template_id, 'name': templates_list[template_id]['name']})
    return jsonify(details)


def get_template():
    global screw_coordinates, start_time, screw_index, results, wait_time
    data = request.get_json()
    template_id = data['id']
    templates_list = read_database()
    screw_coordinates = templates_list[str(template_id)]['screws']
    start_time = 0
    screw_index = 0
    wait_time = 0
    results = []
    return jsonify(templates_list[template_id])

def screwing_process(frame):
    global screw_coordinates, screwdriver_tag_id, start_time, screw_index, wait_time
    if not screw_coordinates:
        # Display message that no template has been selected
        cv2.putText(frame, "Template Error, No Screws Sequence Found", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 255, 0), 2, cv2.LINE_AA)
        return frame
    raw_frame = frame.copy()
    screwdriver_center = np.array([0, 0])
    at_detector = apriltag.Detector()
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
        cv2.circle(frame, (position[0], position[1]), 5, (0, 0, 0), 5)
    nearest_screw = np.argmin(screwdriver_to_screw)
    if screw_index < len(screw_coordinates):
        # 4. Display information and circles, in green 
        cv2.putText(frame, "Next Screw : " + str(screw_index + 1), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0),
                    2,
                    cv2.LINE_AA)
        # Display the type of the next screw
        cv2.putText(frame, "Next Screw Type : " + screw_coordinates[screw_index][2], (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 255, 0), 2,
                    cv2.LINE_AA)
        # #screw that needs to be screwed
        cv2.circle(frame, (screw_coordinates[screw_index][0], screw_coordinates[screw_index][1]), 8, (0, 255, 0), 8)
        # Display the screwdriver center
        cv2.circle(frame, screwdriver_center, 5, (0, 0, 255), 2)
        # Display the nearest screw number
        cv2.putText(frame, "Nearest Screw : " + str(nearest_screw + 1), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 255, 0), 2, cv2.LINE_AA)
        # check if the nearest screw is the next screw to be screwed
        if nearest_screw == screw_index:
            # Draw a circle at the nearest screw
            cv2.circle(frame, (screw_coordinates[nearest_screw][0], screw_coordinates[nearest_screw][1]), 8,
                       (0, 255, 0), 8)
            # check if the screwdriver is close enough to the screw
            if screwdriver_to_screw[nearest_screw] < 30:
                # draw an orange circle on the screw to indicate screwing
                frame = cv2.circle(frame, (screw_coordinates[nearest_screw][0], screw_coordinates[nearest_screw][1]),
                                   radius=8, color=(0, 166, 255), thickness=8)
                # check if start_time has been initialized
                if start_time == 0:
                    start_time = time.time()
                else:
                    elapsed_time = time.time() - start_time
                    # check if the screw has been screwed for 2 seconds
                    if elapsed_time > 2:
                        # delete start_time
                        start_time = 0
                        # increment screw_index
                        screw_index += 1
                        # check if all screws have been screwed
            else:
                # reset start_time
                start_time = 0
        else:
            # reset start_time
            start_time = 0
            # Draw a circle at the nearest screw
            cv2.circle(frame, (screw_coordinates[nearest_screw][0], screw_coordinates[nearest_screw][1]), 8,
                       (0, 0, 255), 8)

        # display green circle on screws that have been screwed
        for i in range(screw_index):
            frame = cv2.circle(frame, (screw_coordinates[i][0], screw_coordinates[i][1]), 8,
                               (255, 255, 255), 8)
    else:
        # break the loop and display message that all screws have been screwed
        # ask to move screwdriver away
        if len(results) == 0:
            if screwdriver_to_screw[nearest_screw] < 200:
                cv2.putText(frame, "Move screwdriver away", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2,
                            cv2.LINE_AA)
                wait_time = 0
            else:
                if wait_time == 0:
                    wait_time = time.time()
                else:
                    elapsed_time = time.time() - wait_time
                    cv2.putText(frame, "Capturing Frame", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2,
                                cv2.LINE_AA)
                    if elapsed_time > 3:
                        wait_time = 0
                        for index, screw in enumerate(screw_coordinates):
                            # check if screw is present using neural network
                            status = verify_screw_presence(raw_frame, screw[0], screw[1])
                            results.append(status)
        else:
            print("Screw Verification Results:", results)
            cv2.putText(frame, "Screw Verification Results:", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2,
                        cv2.LINE_AA)
            for index, screw in enumerate(screw_coordinates):
                status = results[index]
                print(index, screw, status)
                if status == screw[2]:  # Compare the predicted screw type with the expected screw type
                    cv2.putText(frame, str(index + 1) + " Screw " + str(screw) + " is present", (10, index * 30 + 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                    cv2.circle(frame, (screw[0], screw[1]), 8, (0, 255, 0), 8)
                else:
                    cv2.putText(frame, str(index + 1) + " Screw " + str(screw) + " is missing or incorrect",
                                (10, index * 30 + 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                    cv2.circle(frame, (screw[0], screw[1]), 8, (0, 0, 255), 8)
    return frame
