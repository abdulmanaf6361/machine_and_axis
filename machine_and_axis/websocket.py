import asyncio
import websockets
import json

# WebSocket endpoint (adjust based on your setup)
WEBSOCKET_URL = "ws://localhost:8000/ws/machine-data/"

# Sample data that mimics IoT input
sample_data = {
    "machine_id": 1,
    "axis_name": "X",
    "tool_offset": 12.5,
    "feedrate": 10000,
    "tool_in_use": 4,
    "actual_position": 3.9823,
    "target_position": 4.8756,
    "homed": 1,
    "acceleration": 120,
    "velocity": 40
}

async def test_websocket():
    async with websockets.connect(WEBSOCKET_URL) as websocket:
        # Send the sample data to the server
        await websocket.send(json.dumps(sample_data))
        print(f"Sent data: {json.dumps(sample_data)}")

        # Wait for a response from the server
        response = await websocket.recv()
        print(f"Received response: {response}")

# Run the client
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(test_websocket())
