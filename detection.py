# detection.py
from ultralytics import YOLO

# Load model only once
model = YOLO("models/yolov8n.pt")

def run_detection(frame):
    results = model(frame)[0]
    detections = []

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        cls = int(box.cls[0])
        detections.append({
            "bbox": [x1, y1, x2, y2],
            "confidence": conf,
            "class": cls
        })

    return detections
