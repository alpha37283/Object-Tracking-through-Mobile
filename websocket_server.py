# websocket_server.py
import asyncio
import websockets
import json

clients = set()
frame_callback = None

async def handler(websocket):
    print("✅ Laptop: Android connected")
    clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            if data["type"] == "frame" and frame_callback:
                frame_callback(data["data"])  # Base64 JPEG
            elif data["type"] == "sensor":
                print("📡 Sensor:", data["values"])
    except websockets.ConnectionClosed:
        print("❌ Android disconnected")
    finally:
        clients.remove(websocket)

async def send_click(x, y):
    msg = json.dumps({"type": "click", "x": x, "y": y})
    await asyncio.gather(*(c.send(msg) for c in clients if not c.closed))

def set_frame_callback(cb):
    global frame_callback
    frame_callback = cb

def run_server():
    return websockets.serve(handler, "0.0.0.0", 8765)
