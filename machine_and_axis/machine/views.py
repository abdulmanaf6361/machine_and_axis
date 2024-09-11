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



from rest_framework.permissions import IsAdminUser

# ViewSet for user CRUD operations
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Only staff users can access this view


from django.contrib.auth.models import Group

class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

    def get_permissions(self):
        user = self.request.user
        
        # Debugging: Print the user's username and groups
        user_groups = user.groups.all().values_list('name', flat=True)
        print(f"User: {user.username}, Groups: {list(user_groups)}, Action: {self.action}")
        
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            if user.is_staff:
                print(f"User {user.username} is staff. Applying IsSuperAdmin permission.")
                return [IsSuperAdmin()]
            elif user.groups.filter(name='Manager').exists():
                print(f"User {user.username} belongs to Manager group. Applying IsManager permission.")
                return [IsManager()]
            elif user.groups.filter(name='Supervisor').exists():
                print(f"User {user.username} belongs to Supervisor group. Applying IsSupervisor permission.")
                return [IsSupervisor()]
            elif user.groups.filter(name='Operator').exists():
                print(f"User {user.username} belongs to Operator group. Applying IsOperator permission.")
                return [IsOperator()]
        elif self.action in ['retrieve', 'list']:
            print(f"User {user.username} is retrieving or listing. Applying IsAuthenticated permission.")
            return [IsAuthenticated()]
        
        # Default case
        print(f"Default permissions for user {user.username}.")
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
