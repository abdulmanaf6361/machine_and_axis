from rest_framework import serializers
from .models import Machine
from axis.models import Axis

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'

class AxisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Axis
        fields = '__all__'

from django.contrib.auth.models import User, Group
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()  # To show which groups (roles) the user belongs to

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'groups']

    def get_groups(self, obj):
        # Return the names of the groups the user belongs to
        return obj.groups.values_list('name', flat=True)
