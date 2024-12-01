import asyncio
import websockets
import json

async def log_handler(websocket, path):
    """
    Handles incoming logs and prints them in real-time.
    """
    print("WebSocket Server started, waiting for logs...")
    try:
        async for message in websocket:
            log = json.loads(message)
            print(f"\n--- Log Received ---")
            print(f"User: {log['user']}")
            print(f"Script: {log['script']}")
            print(f"Error: {log['error']}")
    except websockets.ConnectionClosed:
        print("Connection closed.")
    except Exception as e:
        print(f"Error in WebSocket Server: {e}")

# Start WebSocket server
start_server = websockets.serve(log_handler, "localhost", 8765)

loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()