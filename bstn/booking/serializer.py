from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

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
    room_type = serializers.CharField()
    room_id = serializers.IntegerField()

    class Meta:
        model = RoomBooking
        fields = [
            'room_type',
            'room_id',
            'check_in',
            'check_out',
        ]

    def validate(self, data):
        room_type = data['room_type']
        room_id = data['room_id']

        # map room_type string -> Model
        room_model_map = {
            'hotelroom': models.HotelRoom,
            'resortroom': models.ResortRoom,
            'homestayroom': models.HomeStayRoom,
        }

        if room_type.lower() not in room_model_map:
            raise serializers.ValidationError('Invalid room type!')
        
        model = room_model_map[room_type.lower()]

        try:
            room_instance = model.objects.get(id=room_id)
        except model.DoesNotExist:
            raise serializers.ValidationError('Room not found!')
        
        data['room_instance'] = room_instance
        return data
    
    def create(self, validated_data):
        room = validated_data['room_instance']
        nights = (validated_data['check_out'] - validated_data['check_in']).days

        # Automatically detects provider
        provider = room.hotel.provider if hasattr(room, 'hotel') else room.homestay.provider if hasattr(room, 'homestay') else room.resort_rooms.provider

        # Total Price
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


