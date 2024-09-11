from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MachineViewSet, AxisViewSet, UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

router = DefaultRouter()
router.register(r'machines', MachineViewSet)
router.register(r'axes', AxisViewSet)
router.register(r'users', UserViewSet)
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(router.urls)),
]

