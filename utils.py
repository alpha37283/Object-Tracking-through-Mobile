import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO("yolov8n.pt") 

def decode_image(jpeg_bytes: bytes):
    nparr = np.frombuffer(jpeg_bytes, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

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

def draw_boxes(frame, detections):
    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        label = f'{det["class"]} {int(det["confidence"] * 100)}%'
        color = tuple(int(x) for x in np.random.default_rng(hash(det["class"]) % (2**32)).integers(0, 255, size=3))
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        cv2.rectangle(frame, (x1, y1 - th - 4), (x1 + tw, y1), color, -1)
        cv2.putText(frame, label, (x1, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    return frame

def scale_bboxes_for_android(detections, x_scale=1.0, y_scale=1.0, pad_x=120):
    scaled = []
    for det in detections:
        x1, y1, x2, y2 = det["bbox"]

        # Apply scaling
        x1 = int(x1 * x_scale)
        y1 = int(y1 * y_scale)
        x2 = int(x2 * x_scale)
        y2 = int(y2 * y_scale)

        # Only widen towards the right
        x2 = x2 + pad_x

        new_det = det.copy()
        new_det["bbox"] = [x1, y1, x2, y2]
        scaled.append(new_det)
    return scaled
