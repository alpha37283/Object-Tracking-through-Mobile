# utils.py
import cv2
import random
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # You can change to yolov8s.pt etc.

# Decode JPEG bytes to OpenCV image
def decode_image(jpeg_bytes: bytes):
    nparr = np.frombuffer(jpeg_bytes, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

# Perform YOLO object detection
def detect_objects(image):
    results = model(image)[0]
    detections = []
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        conf = float(box.conf[0])
        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]
        detections.append({
            "class": class_name,
            "confidence": conf,
            "bbox": [x1, y1, x2, y2]
        })
    return detections

# Draw bounding boxes with labels
def draw_boxes(frame, detections):
    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        label = f'{det["class"]} {int(det["confidence"] * 100)}%'

        # Color based on class name hash
        color = tuple(int(x) for x in np.random.default_rng(hash(det["class"]) % (2**32)).integers(0, 255, size=3))

        # Draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # Draw label background
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        cv2.rectangle(frame, (x1, y1 - th - 4), (x1 + tw, y1), color, -1)

        # Draw label text
        cv2.putText(frame, label, (x1, y1 - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    return frame
