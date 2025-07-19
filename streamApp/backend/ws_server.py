import asyncio
import websockets

mobile_client = None
laptop_client = None

async def handler(websocket):
    global mobile_client, laptop_client
    print(f"New connection from: {websocket.remote_address}")
    try:
        # First message identifies the client role
        role = await websocket.recv()
        print(f"Role received: {role}")
        if role == "mobile":
            mobile_client = websocket
            print("Mobile connected")
        elif role == "laptop":
            laptop_client = websocket
            print("Laptop connected")
        else:
            print(f"Unknown role: {role}")
        # Relay messages between clients
        async for message in websocket:
            print(f"Message received from {role}: type={type(message)}")
            if websocket == mobile_client and laptop_client:
                if isinstance(message, (bytes, bytearray)):
                    await laptop_client.send(message)  # Video frame to laptop
            elif websocket == laptop_client and mobile_client:
                if isinstance(message, str):
                    await mobile_client.send(message)  # Coordinates to mobile
    except websockets.ConnectionClosed:
        print(f"Connection closed for role: {role}")
        if websocket == mobile_client:
            mobile_client = None
            print("Mobile disconnected")
        elif websocket == laptop_client:
            laptop_client = None
            print("Laptop disconnected")
    except Exception as e:
        print(f"Error in handler: {e}")

async def main():
    # Start the WebSocket server and keep it running
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())