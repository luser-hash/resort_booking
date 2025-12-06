from django.db import models
from decimal import Decimal
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from accounts.models import User, ProviderProfile

# Create your models here.


class RoomBooking(models.Model):
    STATUS_CHOICE = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
        ('REJECTED', 'Rejected'),
    ]

    # Who booked
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='room_bookings',
    )

    # Generic reletions to any room type
    # ContentType provides a way to refer to any model class
    # Generic foreign key allows linking to any model instance dynamically
    room_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    room_id = models.PositiveIntegerField()
    room = GenericForeignKey('room_type', 'room_id')

    # Provider
    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name='room_bookings'
    )

    # booking dates
    check_in = models.DateField()
    check_out = models.DateField()

    # money
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )

    # Booking Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICE,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking #{self.id} -> {self.user.full_name} -> {self.room}"