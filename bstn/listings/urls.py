from django.urls import path
from . import api_views


urlpatterns = [
    path('hotels/', api_views.HotelListCreateAPIView.as_view(), name='hotel-list'),
    path('hotels/<int:hotel_id>/rooms/', api_views.HotelRoomListCreateAPIView.as_view(), name='hotelroom-list-create'),
    path('resorts/<int:resort_id>/rooms/', api_views.ResortRoomListCreateAPIView.as_view(), name='resortroom-list-creare'),
    path('resorts/', api_views.ResorTListCreateAPIView.as_view(), name='resort-list-create'),
    path('homestay/', api_views.HomeStayListCreateAPIView.as_view(), name='homestay-list'),
    path('homestay/<int:homestay_id>/rooms/', api_views.HomeStayRoomListCreateAPIView.as_view(), name='homestay-rooms'),
]