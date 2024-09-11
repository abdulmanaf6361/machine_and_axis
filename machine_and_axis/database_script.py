import os
import random
import time
import redis
import json
from django.utils import timezone
import django

# Setup Django environment to use ORM outside of views
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "machine_and_axis.settings")
django.setup()

from machine.models import Machine
from axis.models import Axis

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Constants
MACHINES = 20
AXES = ['X', 'Y', 'Z', 'A', 'C']

# Time intervals (in seconds)
UPDATE_INTERVALS = {
    'tool_offset': 15 * 60,  # Every 15 minutes
    'feedrate': 15 * 60,     # Every 15 minutes
    'tool_in_use': 5 * 60,   # Every 5 minutes
    'actual_position': 0.1,  # Every 0.1 seconds
    'target_position': 0.1,  # Every 0.1 seconds
    'acceleration': 0.1,     # Every 0.1 seconds
    'velocity': 0.1          # Every 0.1 seconds
}

# Sample value ranges for the fields
RANGES = {
    'tool_offset': (5, 40),
    'feedrate': (0, 20000),
    'tool_in_use': (1, 24),
    'actual_position': (-190, 190),
    'target_position': (-190, 191),
    'acceleration': (0, 150),
    'velocity': (0, 80)
}

# Function to generate a random value within a range
def generate_value(field):
    min_val, max_val = RANGES[field]
    return round(random.uniform(min_val, max_val), 4)

# Generate data for each machine and axis
def generate_machine_data(machine_id, axis_name):
    data = {
        'machine_id': machine_id,
        'axis_name': axis_name,
        'tool_offset': generate_value('tool_offset'),
        'feedrate': random.randint(0, 20000),
        'tool_in_use': random.randint(1, 24),
        'actual_position': generate_value('actual_position'),
        'target_position': generate_value('target_position'),
        'homed': random.randint(0, 1),
        'acceleration': random.randint(0, 150),
        'velocity': random.randint(0, 80),
        'max_acceleration': random.randint(0, 150),
        'max_velocity': random.randint(0, 80),
    }
    
    # Convert data to JSON and push to Redis queue
    redis_client.rpush('data_queue', json.dumps(data))

# Main function to generate and save the data
def generate_data():
    start_time = time.time()

    while True:
        current_time = time.time()
        
        # Loop through 20 machines
        for machine_id in range(1, MACHINES + 1):
            # Loop through 5 axes for each machine
            for axis in AXES:
                # Generate the data for the machine and axis
                generate_machine_data(machine_id, axis)

        # Sleep for 0.1 seconds 
        time.sleep(0.1)

        # Print the time elapsed for debugging or stopping the script
        elapsed_time = time.time() - start_time

        # Check to exit after some time (for demonstration, stop after 3 minutes)
        if elapsed_time > 3 * 60:  # Stops after 3 minutes
            break

# Run the data generation script
if __name__ == "__main__":
    generate_data()
    print("done man")