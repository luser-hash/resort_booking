from django.urls import path
from .api_views import RoomBookingListAPIView, RoomBookingCreateAPIView


urlpatterns = [
    path('rooms/', RoomBookingListAPIView.as_view(), name='room-booking-list'),
    path('rooms/room-booking/', RoomBookingCreateAPIView.as_view(), name='room-booking-create'),
]