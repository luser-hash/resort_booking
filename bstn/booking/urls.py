from django.urls import path
from .api_views import (
    RoomBookingListAPIView,
    RoomBookingCreateAPIView,
    MyRoomBookingsAPIView,
    ProviderBookingsAPIView,
    CancelRoomBookingAPIView,
    ConfirmRoomBookingAPIView,
    RejectRoomBookinAPIView,
    )


urlpatterns = [
    path('rooms/', RoomBookingListAPIView.as_view(), name='room-booking-list'),
    path('rooms/room-booking/', RoomBookingCreateAPIView.as_view(), name='room-booking-create'),
    path('rooms/my/', MyRoomBookingsAPIView.as_view(), name='my-room-bookings'),
    path('rooms/provider/<int:provider_id>/', ProviderBookingsAPIView.as_view(), name='Provider-room-bookings-list'),
    path('rooms/<int:booking_id>/cancel', CancelRoomBookingAPIView.as_view(), name='cancel-room-booking'),
    path('rooms/<int:booking_id>/confirm', ConfirmRoomBookingAPIView.as_view(), name='confirm-room-booking'),
    path('rooms/<int:booking_id>/reject', RejectRoomBookinAPIView.as_view(), name='reject-room-booking'),
]