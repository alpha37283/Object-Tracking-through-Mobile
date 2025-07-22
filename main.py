from fastapi import FastAPI, File, UploadFile, WebSocket
from fastapi.responses import HTMLResponse
import numpy as np
import cv2
from ultralytics import YOLO
from tracking import start_tracking

app = FastAPI()

# Load YOLOv8 model
model = YOLO("models/yolov8n.pt")

@app.get("/")
def homepage():
    return HTMLResponse("<h2>Mobile Camera Feed Server is Running</h2>")

@app.post("/detect/")
async def detect_image(file: UploadFile = File(...)):
    """
    Optional POST endpoint to test detection with an uploaded image.
    """
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    results = model(frame)[0]
    detections = []
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        cls = int(box.cls[0])
        detections.append({"bbox": [x1, y1, x2, y2], "confidence": conf, "class": cls})

    return {"detections": detections}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Receives JPEG-encoded frames from the mobile app over WebSocket.
    Sends back detection/tracking metadata as JSON.
    """
    await websocket.accept()
    print("✅ WebSocket connection established")

    try:
        while True:
            # Receive JPEG bytes
            data = await websocket.receive_bytes()
            np_arr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if frame is None:
                print("⚠️ Received empty frame")
                continue

            # Run tracking
            tracked_frame, metadata = start_tracking(frame, model)

            # Optional: You can visualize this frame in a local OpenCV window
            # cv2.imshow("Tracking", tracked_frame)
            # if cv2.waitKey(1) == ord('q'):
            #     break

            # Send only metadata back to mobile
            await websocket.send_json(metadata)

    except Exception as e:
        print("❌ WebSocket disconnected or error occurred:", e)
    finally:
        print("🛑 WebSocket connection closed")
