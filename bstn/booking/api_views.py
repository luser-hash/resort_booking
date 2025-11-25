from rest_framework import generics, permissions
from .models import RoomBooking
from .serializer import RoomBookingSerializer, RoomBookingCreateSerializer


# Read only list for all room bookings
class RoomBookingListAPIView(generics.ListAPIView):
    queryset = RoomBooking.objects.all().order_by('-created_at')
    serializer_class = RoomBookingSerializer


class RoomBookingCreateAPIView(generics.CreateAPIView):
    serializer_class = RoomBookingCreateSerializer
    permission_classes = [permissions.AllowAny]