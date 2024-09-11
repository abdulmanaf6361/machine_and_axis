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


from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']
