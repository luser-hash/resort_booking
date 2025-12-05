from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from datetime import date

from accounts.models import User, ProviderProfile
from listings import models
from .models import RoomBooking


class RoomBookingSerializer(serializers.ModelSerializer):
    room_type_name = serializers.CharField(source='room_type.model', read_only=True)
    
    class Meta:
        model = RoomBooking
        fields = [
            'id',
            'user',
            'provider',
            'room_type',
            'room_type_name',      # ContentType id (internal)
            'room_id',        # actual room primary key
            'check_in',
            'check_out',
            'total_price',
            'status',
            'created_at',
        ]


class RoomBookingCreateSerializer(serializers.ModelSerializer):
    # collecting data from model  
    room_type = serializers.CharField()
    room_id = serializers.IntegerField()

    class Meta:
        # create a room booking object from request body
        model = RoomBooking
        fields = [
            'room_type',
            'room_id',
            'check_in',
            'check_out',
        ]

    def validate(self, data):
        """
        Docstring for validate
        
        Validate room type + room id
        Ensures the room exists
        attach room instance then validate the date.
        Validate date order, no past check in, no zero/negetive nights, 
        overlapping bookings.  
        """
        room_type = data['room_type'].lower()
        room_id = data['room_id']
        check_in = data['check_in']
        check_out = data['check_out']

        # map room_type string -> Model, converts string to model sent by user
        room_model_map = {
            'hotel': models.HotelRoom,
            'hotelroom': models.HotelRoom,
            'resort': models.ResortRoom,
            'resortroom': models.ResortRoom,
            'homestay': models.HomeStayRoom,
            'homestayroom': models.HomeStayRoom,
        }

        if room_type not in room_model_map:
            raise serializers.ValidationError('Invalid room type!')
        
        # pick the model based on type
        model = room_model_map[room_type]

        try:
            room_instance = model.objects.get(id=room_id)
        except model.DoesNotExist:
            raise serializers.ValidationError('Room not found!')
        
        data['room_instance'] = room_instance

        # Date Validation
        # 1. Check out must be after check in, means check_out > check_in
        if check_out <= check_in:
            raise serializers.ValidationError('Check out must be after check in!')
        
        # 2. check in cannot be past, means check_in >= today
        if check_in < date.today():
            raise serializers.ValidationError('Check in cannot be past date!')
        
        # 3. Check overlapping bookings for this same room
        existing_booking = RoomBooking.objects.filter(
            room_type=ContentType.objects.get_for_model(room_instance),
            room_id=room_instance.id,
            status__in=['PENDING', 'CONFIRMED'],  # Only active bookings
        ).filter(
            check_in__lt=check_out,
            check_out__gt=check_in,
        )

        if existing_booking.exists():
            raise serializers.ValidationError('This room is already booked for the selected days!')

        return data
    
    def create(self, validated_data):
        room = validated_data['room_instance']
        nights = (validated_data['check_out'] - validated_data['check_in']).days

        # Automatically detects provider
        provider = room.provider
        if provider is None:
            raise Exception("Room has no provider linked!")
        
        # calculate the total price
        total_price = room.price_per_night * nights

        # Create Booking
        booking = RoomBooking.objects.create(
            user=self.context['request'].user,
            provider=provider,
            room_type=ContentType.objects.get_for_model(room),
            room_id=room.id,
            check_in=validated_data['check_in'],
            check_out=validated_data['check_out'],
            total_price=total_price,
        )

        return booking


class GuestMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'email',
        ]


class ProviderMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderProfile
        fields = [
            'id',
            'display_name',
        ]


class BookingDetailSerializer(serializers.ModelSerializer):
    guest = GuestMiniSerializer(source='user', read_only=True)
    provider = ProviderMiniSerializer(read_only=True)
    room = serializers.SerializerMethodField()
    nights = serializers.SerializerMethodField()

    class Meta:
        model = RoomBooking
        fields = [
            'id',
            'status',
            'total_price',
            'check_in',
            'check_out',
            'nights',
            'guest',
            'provider',
            'room',
            'created_at',
        ]

    def get_nights(self, obj):
        return (obj.check_out - obj.check_in).days
    
    def get_room(self, obj):
        room = obj.room 
        
        if room is None:
            return None
        
        # determine room type + parent stay
        if hasattr(room, 'hotel'):
            room_type = 'hotel'
            stay = room.hotel
        elif hasattr(room, 'resort'):
            room_type = 'resort'
            stay = room.resort
        elif hasattr(room, 'homestay'):
            room_type = 'homestay'
            stay = room.homestay
        else:
            room_type = 'unknown'
            stay = None

        stay_data = None
        if stay is None:
            stay_data = {
                'id': stay.id,
                'name': getattr(stay, 'name', ''),
                'city': getattr(stay, 'city', ''),
                'contry': str(getattr(stay, 'country', '')),
            }
        
        return {
            'id': room.id,
            'name': getattr(room, 'room_name', ''),
            'type': room_type,
            'price_per_night': room.price_per_night,
            'max_guest': room.max_guest_per_room,
            'stay': stay_data,
        }