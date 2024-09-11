import json
import redis
from channels.generic.websocket import WebsocketConsumer

# Setup Redis connection
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

class MachineDataConsumer(WebsocketConsumer):
    
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        # Incoming data in JSON format from IoT source
        data = json.loads(text_data)
        
        # Example: You can do validation here to ensure data structure integrity
        machine_id = data.get('machine_id')
        axis_name = data.get('axis_name')
        
        # Ensure valid data
        if machine_id and axis_name:
            # Push the incoming data to the Redis queue
            redis_client.rpush('data_queue', json.dumps(data))
            print(f"Data pushed to Redis: {data}")

            # Optionally send back a confirmation to the WebSocket client
            self.send(text_data=json.dumps({'status': 'received', 'data': data}))
        else:
            # Send error message if the data is not valid
            self.send(text_data=json.dumps({'status': 'error', 'message': 'Invalid data received'}))
