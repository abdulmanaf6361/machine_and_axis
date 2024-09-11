from rest_framework import viewsets
from .models import Machine
from axis.models import Axis
from .serializers import MachineSerializer, AxisSerializer
from .permissions import IsSuperAdmin, IsManager, IsSupervisor, IsOperator
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer



# ViewSet for user CRUD operations
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            if self.request.user.is_staff:
                return [IsSuperAdmin()]
            elif self.request.user.groups.filter(name='Manager').exists():
                return [IsManager()]
            elif self.request.user.groups.filter(name='Supervisor').exists():
                return [IsSupervisor()]
            elif self.request.user.groups.filter(name='Operator').exists():
                return [IsOperator()]
        elif self.action == 'retrieve' or self.action == 'list':
            return [IsAuthenticated()]
        return super().get_permissions()

class AxisViewSet(viewsets.ModelViewSet):
    queryset = Axis.objects.all()
    serializer_class = AxisSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            if self.request.user.is_staff:
                return [IsSuperAdmin()]
            elif self.request.user.groups.filter(name='Manager').exists():
                return [IsManager()]
            elif self.request.user.groups.filter(name='Supervisor').exists():
                return [IsSupervisor()]
            elif self.request.user.groups.filter(name='Operator').exists():
                return [IsOperator()]
        elif self.action == 'retrieve' or self.action == 'list':
            return [IsAuthenticated()]
        return super().get_permissions()
