from rest_framework.permissions import BasePermission
from accounts.models import ProviderProfile, GuestProfile


class IsGuest(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return GuestProfile.objects.filter(user=request.user).exists()
    

class IsProvider(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return ProviderProfile.objects.filter(user=request.user).exists()
    

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.is_staff or request.user.is_superuser)
        )