# views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Axis
from .serializers import AxisSerializer
from django.utils import timezone
from datetime import timedelta

class AxisHistoricalDataView(generics.ListAPIView):
    serializer_class = AxisSerializer

    def get_queryset(self):
        now = timezone.now()
        fifteen_minutes_ago = now - timedelta(minutes=15)
        
        axis_names = self.request.query_params.getlist('axis_names', [])
        
        queryset = Axis.objects.filter(created_at__gte=fifteen_minutes_ago)
        
        if axis_names:
            queryset = queryset.filter(axis_name__in=axis_names)
        
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
