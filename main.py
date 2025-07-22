# main.py
from fastapi import FastAPI, File, UploadFile, WebSocket
from fastapi.responses import HTMLResponse
import numpy as np
import cv2
from detection import run_detection
from utils import draw_boxes

app = FastAPI()

@app.get("/")
def homepage():
    return HTMLResponse("<h2>Mobile Camera Feed Server is Running</h2>")

@app.post("/detect/")
async def detect_image(file: UploadFile = File(...)):
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    detections = run_detection(frame)
    return {"detections": detections}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connection accepted")

    window_name = "Mobile Stream"
    cv2.namedWindow(window_name)

    while True:
        try:
            data = await websocket.receive_bytes()

            np_arr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

            if frame is not None:
                # Run detection and draw bounding boxes
                detections = run_detection(frame)
                frame_with_boxes = draw_boxes(frame, detections)

                # Show annotated frame
                display_frame = cv2.resize(frame_with_boxes, (960, 720)) 
                cv2.imshow(window_name, frame_with_boxes)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

        except Exception as e:
            print("❌ Error in WebSocket:", e)
            break

    cv2.destroyAllWindows()
