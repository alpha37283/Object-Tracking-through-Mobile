from fastapi import FastAPI, File, UploadFile, WebSocket
from fastapi.responses import HTMLResponse
import cv2
import numpy as np
from ultralytics import YOLO
from tracking import start_tracking

app = FastAPI()
model = YOLO("models/yolov8n.pt")

@app.get("/")
def homepage():
    return HTMLResponse(open("static/index.html").read())

@app.post("/detect/")
async def detect_image(file: UploadFile = File(...)):
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
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        np_arr = np.frombuffer(data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        tracked_frame, metadata = start_tracking(frame, model)
        # Here: compress tracked_frame to JPEG and send back (optional)

        await websocket.send_json(metadata)
