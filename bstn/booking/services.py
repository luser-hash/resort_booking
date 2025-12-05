# booking/services.py
from datetime import date
from .models import RoomBooking


def auto_complete_finished_bookings():
    today = date.today()
    # All CONFIRMED bookings whose stay has ended
    RoomBooking.objects.filter(
        status='CONFIRMED',
        check_out__lt=today,
    ).update(status='COMPLETED')
