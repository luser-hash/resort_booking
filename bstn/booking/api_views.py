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


class MyRoomBookingsAPIView(generics.ListAPIView):
    serializer_class = RoomBookingSerializer
    permission_classes = [permissions.IsAuthenticated] 
    # only logged in user can see their bookings

    # get_queryset narrows to bookings of 'request.user'
    def get_queryset(self):
        return RoomBooking.objects.filter(
            user=self.request.user
        ).order_by('-created_at') 
    

class ProviderBookingsAPIView(generics.ListAPIView):
    serializer_class = RoomBookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        provider_id = self.kwargs['provider_id']
        return RoomBooking.objects.filter(
            provider_id=provider_id
        ).order_by('-created_at')
