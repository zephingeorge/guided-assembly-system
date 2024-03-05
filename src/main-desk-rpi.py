import time
import cv2
import numpy as np
import apriltag

cap = cv2.VideoCapture(0)

# Detector#############################################################
at_detector = apriltag.Detector()

# Define screw coordinates
screw_coordinates = [
    [270, 235],
    [420, 320],
    [420, 235],
    [270, 320],
]

screwdriver_tagid = 3
screwdriver_center = np.array([0, 0])
screw_index = 0

while True:
    # Read a frame from the video
    ret, image = cap.read()
    if not ret:
        break
        # display text for next screw to be screwed
    cv2.putText(image, "Next Screw : " + str(screw_index + 1), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (0, 255, 0), 2, cv2.LINE_AA)

    # display green highlight on next screw
    image = cv2.circle(image, (
        screw_coordinates[screw_index][0], screw_coordinates[screw_index][1]), 8,
                       (0, 255, 0), 2)
    # find position of screwdriver
    tags = at_detector.detect(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    for tag in tags:
        # print(tag.tag_id)
        if tag.tag_id == screwdriver_tagid:
            screwdriver_center = tag.center
            screwdriver_center = (int(screwdriver_center[0]), int(screwdriver_center[1]))
            cv2.circle(image, screwdriver_center, 5, (0, 0, 255), 2)
            screwdriver_center = np.array(screwdriver_center)
            # print("Screwdriver position:", screwdriver_center)
            break
    screwdriver_to_screw = []

    # calculate distance between screwdriver and screws
    for index, position in enumerate(screw_coordinates):
        x, y = position  # Unpack x and y coordinates
        image = cv2.circle(image, (x, y), radius=0, color=(0, 0, 0), thickness=2)
        screw_center = np.array([x, y])
        screwdriver_to_screw.append(np.linalg.norm(screwdriver_center - screw_center))

    # find the index of the nearest screw
    nearest_screw = np.argmin(screwdriver_to_screw)

    # display text to indicate nearest screw
    cv2.putText(image, "Nearest Screw : " + str(nearest_screw + 1), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (0, 255, 0), 2, cv2.LINE_AA)

    # Draw a circle at the nearest screw
    image = cv2.circle(image, (screw_coordinates[nearest_screw][0], screw_coordinates[nearest_screw][1]), radius=0,
                       color=(0, 0, 255), thickness=5)

    # check if the nearest screw is the next screw to be screwed
    if nearest_screw == screw_index:
        # check if the screwdriver is close enough to the screw
        if screwdriver_to_screw[nearest_screw] < 30:
            # draw a orange circle on the screw to indicate screwing
            image = cv2.circle(image, (screw_coordinates[nearest_screw][0], screw_coordinates[nearest_screw][1]),
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
                        cv2.putText(image, "All screws have been screwed", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                    (0, 255, 0), 2, cv2.LINE_AA)
                        break
    # display green circle on screws that have been screwed
    for i in range(screw_index):
        image = cv2.circle(image, (screw_coordinates[i][0], screw_coordinates[i][1]), 8,
                           (0, 255, 0), 8)
    # display the output image
    cv2.imshow('Desk Image', image)

    # Check for key events
    key = cv2.waitKey(1)
    # Break the loop on 'Esc' key or 'q' key
    if key == 27 or key == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()