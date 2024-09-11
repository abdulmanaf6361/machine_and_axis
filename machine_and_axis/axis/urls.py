# urls.py
from django.urls import path
from .views import AxisHistoricalDataView

urlpatterns = [
    path('axis-historical-data/', AxisHistoricalDataView.as_view(), name='axis-historical-data'),
]
