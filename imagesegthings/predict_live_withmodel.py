import cv2
from ultralytics import YOLO
import numpy as np

# Load your trained YOLO segmentation model
model = YOLO("runs/segment/actual_segmentation_500epochs/weights/best.pt")  # ← Update this path!

# Open camera (0 = default webcam, 1 = second camera, etc.)
cap = cv2.VideoCapture(1)

# Check if camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

# Set camera resolution (optional, improves speed)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Press 'q' to quit, 's' to save a snapshot")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Can't receive frame")
        break

    # Run YOLO segmentation inference
    # conf=0.5 = minimum confidence threshold
    # iou=0.7 = NMS IoU threshold
    results = model(frame, conf=0.5, iou=0.7, verbose=False)

    # Plot segmentation masks on the frame
    annotated_frame = results[0].plot()

    # Display FPS (optional)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cv2.putText(annotated_frame, f"FPS: {fps:.1f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the resulting frame
    cv2.imshow('YOLO Segmentation - Live', annotated_frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Press 's' to save a snapshot
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite('snapshot.png', annotated_frame)
        print("Snapshot saved!")

# Cleanup
cap.release()
cv2.destroyAllWindows()
print("Live segmentation stopped.")