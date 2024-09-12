import random
import time
import csv
from datetime import datetime

# Constants
MACHINES = 20
AXES = ['X', 'Y', 'Z', 'A', 'C']
UPDATE_INTERVALS = {
    'tool_offset': 15 * 60,  # Every 15 minutes
    'feedrate': 15 * 60,     # Every 15 minutes
    'tool_in_use': 5 * 60,   # Every 5 minutes
    'actual_position': 0.1,  # Every 0.1 seconds
    'target_position': 0.1,  # Every 0.1 seconds
    'distance_to_go': 0.1,   # Every 0.1 seconds
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

# Generate data for each machine
def generate_machine_data(machine_id, axis_name):
    machine_data = {
        'machine_id': machine_id,
        'machine_name': f'EMXP{machine_id}',
        'tool_capacity': 24,
        'tool_offset': generate_value('tool_offset'),
        'feedrate': random.randint(0, 20000),
        'tool_in_use': random.randint(1, 24),
        'axis_name': axis_name,
        'actual_position': generate_value('actual_position'),
        'target_position': generate_value('target_position'),
        'distance_to_go': generate_value('target_position') - generate_value('actual_position'),
        'homed': random.randint(0, 1),
        'acceleration': random.randint(0, 150),
        'velocity': random.randint(0, 80)
    }
    return machine_data

# Write the generated data to a CSV
def write_to_csv(data, filename="machine_axis_data.csv"):
    fieldnames = [
        'timestamp', 'machine_id', 'machine_name', 'tool_capacity', 'tool_offset', 'feedrate', 'tool_in_use',
        'axis_name', 'actual_position', 'target_position', 'distance_to_go', 'homed', 'acceleration', 'velocity'
    ]
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerows(data)

# Main function to generate the data
def generate_data():
    start_time = time.time()

    # CSV Initialization
    fieldnames = [
        'timestamp', 'machine_id', 'machine_name', 'tool_capacity', 'tool_offset', 'feedrate', 'tool_in_use',
        'axis_name', 'actual_position', 'target_position', 'distance_to_go', 'homed', 'acceleration', 'velocity'
    ]
    
    # Write header in the CSV
    with open("machine_axis_data.csv", mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

    while True:
        current_time = time.time()
        data = []
        # Loop through 20 machines
        for machine_id in range(1, MACHINES + 1):
            # Loop through 5 axes for each machine
            for axis in AXES:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Generate the data for the machine and axis
                machine_data = generate_machine_data(machine_id, axis)
                machine_data['timestamp'] = timestamp
                data.append(machine_data)

        # Write the generated data to CSV
        write_to_csv(data)

        # Sleep for 0.1 seconds (since the smallest interval is 0.1 seconds)
        time.sleep(0.1)

        # Print the time elapsed for debugging or stopping the script
        elapsed_time = time.time() - start_time
        print(f"Time elapsed: {elapsed_time:.2f} seconds")

        # Check to exit after some time (for demonstration, stop after 5 minutes)
        if elapsed_time > 5 * 60:  # Stops after 5 minutes
            break

# Run the data generation script
if __name__ == "__main__":
    generate_data()
