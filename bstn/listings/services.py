from collections import defaultdict
from django.contrib.contenttypes.models import ContentType
from booking.models import RoomBooking
from .models import HotelRoom, ResortRoom, HomeStayRoom


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


def search_availability_stay(check_in, check_out, room_type=None, city=None):
    """
    Docstring for search_availability_stay

    Return a list of stay summaries that have at least one available room
    in the given date range. 
    """

    # Which room models to include
    CONFIG = {
        'hotel': {
            'room_model': HotelRoom,
            'stay_attr': 'hotel',
            'type_label': 'hotel',
        },
        'homestay': {
            'room_model': HomeStayRoom,
            'stay_attr': 'homestay',
            'type_label': 'homestay',
        },
        'resort': {
            'room_model': ResortRoom,
            'stay_attr': 'resort',
            'type_label': 'resort'
        },
    }

    # restrict to one type if room type is provided
    if room_type:
        room_type = room_type.lower()
        if room_type not in CONFIG:
            raise ValueError('Invalid room type')
        types_to_use = [room_type]

    # stay_id -> summary data
    stays = {}

    for key in types_to_use:
        cfg = CONFIG[key]
        room_model = cfg['room_model']
        stay_attr = cfg['stay_attr']
        type_label = cfg['type_label']

        # use existing availability engine
        available_rooms = get_available_rooms_for_model(room_model)

        # for each available room
        # find it's parent stay, applies filter, group by stay, returns a list
        for room in available_rooms:
            stay = getattr(room, stay_attr)

            # city filter if provided
            if city:
                if getattr(stay, 'city', '').lower() != city.lower():
                    continue

            stay_id = stay.id

            if stay_id not in stays:
                stays[stay_id] = {
                    'id': stay.id,
                    'type': type_label,
                    'name': getattr(stay, 'name', ''),
                    'city': getattr(stay, 'city', ''),
                    'price_per_night': room.price_per_night,
                    'available_room_count': 1,
                }
            else:
                s = stays[stay_id]
                s['available_room_count'] += 1
                
    # Return as list
    return list(stays.values())


