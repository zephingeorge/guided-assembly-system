import cv2
import pyzbar.pyzbar as pyzbar

# Open the default webcam (replace 0 with your desired camera index if needed)
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert frame to grayscale for better barcode detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Decode barcodes
    barcodes = pyzbar.decode(gray)

    # Process and display the decoded data
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        barcode_data = barcode.data.decode("utf-8")
        print(f"Decoded barcode: {barcode_data}")

        # Add text overlay for the barcode data (optional)
        cv2.putText(frame, barcode_data, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Barcode Scanner', frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) == ord('q'):
        break

# Release capture and close all windows
cap.release()
cv2.destroyAllWindows()
