from django.urls import path
from .auth_views import RegisterAPIView, BecomeProviderAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='auth-register'),
    path('become-provider/', BecomeProviderAPIView.as_view(), name='auth-become-provider'),
]