import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Machine
from axis.models import Axis

class MachineConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        
        # Broadcast current values for all machines and their axes
        machine_data = []
        machines = Machine.objects.all()
        for machine in machines:
            axes = Axis.objects.filter(machine=machine)
            axis_data = [
                {
                    "axis_name": axis.axis_name,
                    "actual_position": axis.actual_position,
                    "target_position": axis.target_position,
                    "velocity": axis.velocity,
                    "acceleration": axis.acceleration,
                }
                for axis in axes
            ]
            machine_data.append({
                "machine_id": machine.machine_id,
                "machine_name": machine.machine_name,
                "axis_data": axis_data
            })
        
        self.send(text_data=json.dumps({
            "machines": machine_data
        }))
