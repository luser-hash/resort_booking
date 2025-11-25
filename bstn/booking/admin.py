from django.contrib import admin
from .models import RoomBooking

# Register your models here.


@admin.register(RoomBooking)
class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'provider', 'check_in', 'check_out', 'status', 'total_price')
    list_filter = ('status', 'check_in', 'check_out')
    search_fields = ('user__full_name', 'room_id', 'provider__display_name')
