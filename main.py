import json
import cv2
import numpy as np
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from utils import decode_image, detect_objects, draw_boxes, scale_bboxes_for_android

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connected")

    while True:
        try:
            data = await websocket.receive_bytes()

            frame = decode_image(data)
            if frame is None:
                continue

            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

            # Frame resolution info
            # height, width = frame.shape[:2]
            # print(f"Frame shape: {width}x{height}")

            # Detect objects
            detections = detect_objects(frame)

            # Draw original boxes locally
            draw_boxes(frame, detections)

            # Send scaled boxes to Android (adjust scale as needed)
            x_scale = 0.8   # Try 0.8 or other if Android is wider
            y_scale = 0.75   # Try <1.0 if Android is cutting top/bottom
            scaled_detections = scale_bboxes_for_android(detections, x_scale, y_scale)

            cv2.imshow("Laptop Debug View", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            await websocket.send_text(json.dumps({"detections": scaled_detections}))

        except Exception as e:
            print(f"Error: {e}")
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8765)
