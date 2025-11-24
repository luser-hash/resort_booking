from django.urls import path
from .api_views import UserListCreateAPIView, ProviderListCreateAPIView, GuestListCreateAPIView

urlpatterns = [
    path('user/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('providers/', ProviderListCreateAPIView.as_view(), name='provider-list-create'),
    path('guests/', GuestListCreateAPIView.as_view(), name='guest-list-create'),
]