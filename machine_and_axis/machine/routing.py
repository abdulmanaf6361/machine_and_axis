from django.urls import re_path
from .consumers import MachineDataConsumer

websocket_urlpatterns = [
    re_path(r'ws/machine-data/', MachineDataConsumer.as_asgi()),
]
