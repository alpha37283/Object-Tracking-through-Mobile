import cv2
import numpy as np

# Dummy implementation
def start_tracking(frame, model):
    results = model.track(source=frame, persist=True, stream=False)
    metadata = []
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            obj_id = int(box.id[0]) if box.id is not None else None
            metadata.append({
                "bbox": [x1, y1, x2, y2],
                "id": obj_id,
                "class": int(box.cls[0]),
                "conf": float(box.conf[0])
            })
    return frame, metadata
