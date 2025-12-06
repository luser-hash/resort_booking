from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, BecomeProviderSerializer, CustomTokenObtainPairSerializer
from .models import ProviderProfile

User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class BecomeProviderAPIView(generics.CreateAPIView):
    """
    Requires the user to be logged in.
    on success returned the created provider profile JSON
    """
    serializer_class = BecomeProviderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProviderProfile.objects.all()
    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer