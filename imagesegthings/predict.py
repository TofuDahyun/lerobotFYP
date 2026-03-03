from ultralytics import YOLO

# Load a model
model = YOLO("runs/segment/actual_segmentation_500epochs/weights/best.pt")  # pretrained YOLO26n model

# Run batched inference on a list of images
results = model(["test_images/clear_3.jpg"])  # return a list of Results objects

# #test
# model = YOLO("yolo26n.pt")
# results = model("https://ultralytics.com/images/bus.jpg")


# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    result.show()  # display to screen
    result.save(filename="result.jpg")  # save to disk