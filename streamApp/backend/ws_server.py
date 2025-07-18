import asyncio
import websockets

mobile_client = None
laptop_client = None

async def handler(websocket):
    global mobile_client, laptop_client
    try:
        # First message identifies the client role
        role = await websocket.recv()
        if role == "mobile":
            mobile_client = websocket
            print("Mobile connected")
        elif role == "laptop":
            laptop_client = websocket
            print("Laptop connected")
        
        # Relay messages between clients
        async for message in websocket:
            if websocket == mobile_client and laptop_client:
                await laptop_client.send(message)  # Video frame to laptop
            elif websocket == laptop_client and mobile_client:
                await mobile_client.send(message)  # Coordinates to mobile
    except websockets.ConnectionClosed:
        if websocket == mobile_client:
            mobile_client = None
            print("Mobile disconnected")
        elif websocket == laptop_client:
            laptop_client = None
            print("Laptop disconnected")

async def main():
    # Start the WebSocket server and keep it running
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())