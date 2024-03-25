import cv2

# Create Aruco detector object (adapting for your OpenCV version)
if hasattr(cv2.aruco, "createDetector"):  # OpenCV 4.5 and above
    detector = cv2.aruco.createDetector(cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_250))
else:
    detector = cv2.aruco.ArucoDetector(cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250))

# Create video capture object using your camera index (usually 0)
cap = cv2.VideoCapture(0)

while True:
  # Capture frame-by-frame
  ret, frame = cap.read()

  # Check if frame is captured successfully
  if not ret:
    print("Error: Unable to capture frame from camera")
    break

  # Detect Aruco markers in the frame
  corners, ids, rejected = detector.detectMarkers(frame)

  # Draw detected markers (optional)
  if ids is not None:
    # Draw a polygon around each detected marker
    for i, corner in enumerate(corners):
      cv2.polylines(frame, [corner.astype(int)], True, (0, 255, 0), 2)

    # Print detected Aruco IDs
    for i, id in enumerate(ids):
      print(f"Aruco marker ID detected: {id[0]}")
    # Mark center of the aruco marker
    for i, corner in enumerate(corners):
      x = int((corner[0][0][0] + corner[0][2][0]) / 2)
      y = int((corner[0][0][1] + corner[0][2][1]) / 2)
      cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

  # Display the resulting frame
  cv2.imshow('Aruco Marker Detection', frame)

  # Exit loop on 'q' key press
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# Release capture and close all windows
cap.release()
cv2.destroyAllWindows()
