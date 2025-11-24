from rest_framework import generics
from .models import ProviderProfile, GuestProfile, User
from .serializers import UserMiniSerializer, ProviderProfileserializer, GuestProfileSerializer

# Generic views allows build API views map closely to database models.


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserMiniSerializer


class ProviderListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProviderProfile.objects.all()
    serializer_class = ProviderProfileserializer

    # This gives: GET -> list all providers, POST -> Create a new 


class GuestListCreateAPIView(generics.ListCreateAPIView):
    queryset = GuestProfile.objects.all()
    serializer_class = GuestProfileSerializer


