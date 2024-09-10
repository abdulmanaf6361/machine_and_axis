import redis
import json
import django
import os
import time

# Setup Django environment to use ORM outside of views
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "machine_and_axis.settings")
django.setup()

from machine.models import Machine
from axis.models import Axis

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def write_to_database(data):
    data = json.loads(data)
    machine, created = Machine.objects.get_or_create(
        machine_id=data['machine_id'],
        defaults={
            'machine_name': f'EMXP{data["machine_id"]}',
            'tool_capacity': 24,
            'tool_offset': data['tool_offset'],
            'feedrate': data['feedrate'],
            'tool_in_use': data['tool_in_use'],
        }
    )

    axis = Axis(
        machine=machine,
        axis_name=data['axis_name'],
        actual_position=data['actual_position'],
        target_position=data['target_position'],
        distance_to_go=data['distance_to_go'],
        homed=data['homed'],
        acceleration=data['acceleration'],
        velocity=data['velocity'],
        max_acceleration=data['max_acceleration'],
        max_velocity=data['max_velocity']
    )
    axis.save()

def process_queue():
    while True:
        # Pop data from Redis queue
        data = redis_client.lpop('data_queue')
        if data:
            # Process and write data to database
            write_to_database(data)
        else:
            # Sleep for a while to avoid busy waiting
            time.sleep(0.1)

# Run the data processor
if __name__ == "__main__":
    process_queue()
