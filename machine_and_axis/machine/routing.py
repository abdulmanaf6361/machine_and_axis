from django.urls import re_path
from .consumers import MachineConsumer

websocket_urlpatterns = [
    re_path(r'ws/machines/', MachineConsumer.as_asgi()),
]
