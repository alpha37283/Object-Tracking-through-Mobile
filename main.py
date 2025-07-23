import json
import cv2
import numpy as np
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from utils import decode_image, detect_objects, draw_boxes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ WebSocket connected")

    while True:
        try:
            data = await websocket.receive_bytes()

            # Decode JPEG to OpenCV frame
            frame = decode_image(data)
            if frame is None:
                continue

            # Rotate the frame
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

            # frame shape 
            print(f"Frame shape: {frame.shape}")  # Debugging line

            #frame = cv2.resize(frame, (1080, 2400)) 

            # Detect objects
            detections = detect_objects(frame)

            # Draw bounding boxes on the frame
            frame = draw_boxes(frame, detections)

            # Display the annotated frame (non-blocking)
            cv2.imshow("YOLOv8 Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Send back detections as JSON
            await websocket.send_text(json.dumps({"detections": detections}))

        except Exception as e:
            print(f"❌ Error: {e}")
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8765)
