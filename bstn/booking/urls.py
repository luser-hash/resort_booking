from django.urls import path
from .api_views import (
    RoomBookingListAPIView,
    RoomBookingCreateAPIView,
    MyRoomBookingsAPIView,
    ProviderBookingsAPIView,
    )


urlpatterns = [
    path('rooms/', RoomBookingListAPIView.as_view(), name='room-booking-list'),
    path('rooms/room-booking/', RoomBookingCreateAPIView.as_view(), name='room-booking-create'),
    path('rooms/my/', MyRoomBookingsAPIView.as_view(), name='my-room-bookings'),
    path('rooms/provider/<int:provider_id>/', ProviderBookingsAPIView.as_view(), name='Provider-room-bookings-list'),
]