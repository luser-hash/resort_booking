from django.urls import path
from .auth_views import RegisterAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='auth-register'),
]