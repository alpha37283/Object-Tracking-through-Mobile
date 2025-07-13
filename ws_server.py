import asyncio
import websockets
import json

clients = set()

async def handler(websocket):
    clients.add(websocket)
    print("Client connected")
    try:
        async for message in websocket:
            data = json.loads(message)

            if data.get("type") == "frame":
                print("Received frame")

            if data.get("type") in ["frame", "click"]:
                for client in clients:
                    if client != websocket and client.open:
                        await client.send(json.dumps(data))

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server started at ws://0.0.0.0:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
