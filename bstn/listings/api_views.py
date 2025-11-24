from rest_framework import generics
from . import serializers
from . import models


class HotelListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Hotel.objects.all()
    serializer_class = serializers.HotelSerializer


class HotelRoomListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.HotelRoom.objects.all()
    serializer_class = serializers.HotelRoomSerializer


class ResortRoomListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.ResortRoom.objects.all()
    serializer_class = serializers.ResortRoomSerializer


class ResorTListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Resort.objects.all()
    serializer_class = serializers.ResortSerializer


class HomeStayListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.HomeStay.objects.all()
    serializer_class = serializers.HomeStaySerializer


class HomeStayRoomListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.HomeStayRoom.objects.all()
    serializer_class = serializers.HomeStayRoomSerializer
    
    

