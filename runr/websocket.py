import json
import asyncio
from websockets import connect as ws_connect

async def log_error_async(user_name, r_script, error_message):
    """
    Sends error logs to the WebSocket server.
    """
    log_data = {
        'user': user_name,
        'script': r_script,
        'error': error_message,
    }
    try:
        ws_url = "ws://localhost:8765"  # Replace with your WebSocket server address if needed
        async with ws_connect(ws_url) as websocket:
            await websocket.send(json.dumps(log_data))
    except Exception as e:
        # Optionally log locally for debugging purposes
        print(f"Failed to send log via WebSocket: {e}")

def log_error(user_name, r_script, error_message):
    """
    Wrapper to run async log_error_async in a blocking context.
    """
    asyncio.run(log_error_async(user_name, r_script, error_message))
