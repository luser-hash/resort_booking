from django.contrib.contenttypes.models import ContentType
from booking.models import RoomBooking


def get_available_rooms_for_model(room_model, check_in, check_out):
    """
    Docstring for get_available_rooms_for_model.
    This is a helper/utility function to get all available rooms for any room model.
    Args:
        room_model: The room model class
        check_in: date object for check in date
        check_out: date object for check out date

    This is the core availabilty engine for any room model.

    What it does:
        1. Get content type for the room model
        2. Query RoomBooking to find all booked rooms of this type that overlap with the requested date range
        3. Exclude these booked rooms from the room model's objects to get available rooms
        4. Return the available rooms queryset        
   """

    # get room content type 
    room_ct = ContentType.objects.get_for_model(room_model)

    # get id for booked rooms of this type
    booked_rooms_id = RoomBooking.objects.filter(
        room_type=room_ct,
        status__in=['PENDING', 'CONFIRMED'],
        check_in__lt=check_out,
        check_out__gt=check_in,
    ).values_list('room_id', flat=True)

    # get available rooms by excluding booked ones
    return room_model.objects.exclude(id__in=booked_rooms_id)