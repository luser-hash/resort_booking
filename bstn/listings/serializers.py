from rest_framework import serializers
from .models import Hotel, HotelRoom, Resort, ResortRoom, HomeStay, HomeStayRoom
from accounts.models import ProviderProfile


class ProviderMiniSerizalizer(serializers.ModelSerializer):
    class Meta:
        model = ProviderProfile
        fields = ['id', 'display_name', 'phone', 'city', 'country']


class HotelRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRoom
        fields = [
            'id',
            'hotel',
            'room_name',
            'room_type',
            'max_guest_per_room',
            'price_per_night',
            'room_utils',
            'amenities',
            'is_available',
            'has_ac',
            'has_heating',
        ]


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = [
            'id',
            'provider',
            'name',
            'description',
            'total_rooms',
            'check_in_time',
            'check_out_time',
            'address',
            'city',
            'country',
            'has_wifi',
            'has_parking',
            'has_kitchen',
            'pets_allowed',
            'image',
            'is_active',
            'star_rating',
            'has_room_service',
            'has_reception_24h',
            'has_elevator',
            'has_restaurant',
            'allows_walk_in',
            
        ]


class ResortRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResortRoom
        fields = [
            'id',
            'resort',
            'room_name',
            'villa_type',
            'max_guest_per_room',
            'price_per_night',
            'room_utils',
            'amenities',
            'is_available',
            'has_ac',
            'has_heating',
        ]


class ResortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resort
        fields = [
            'id',
            'provider',
            'name',
            'description',
            'total_rooms',
            'check_in_time',
            'check_out_time',
            'address',
            'city',
            'country',
            'has_wifi',
            'has_parking',
            'has_kitchen',
            'pets_allowed',
            'image',
            'is_active',
            'star_rating',
            'has_room_service',
            'num_of_pools',
            'has_spa',
            'has_gym',
            'has_sports_center',
            'has_golf_course',
            'dining_type',
            'dining_options_count',
            'has_buffet',
            'has_bar',
            'activities_description',
            'is_all_inclusive_available',
            'all_inclusive_details',
        ]


class HomeStaySerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeStay
        fields = [
            'id',
            'provider',
            'name',
            'description',
            'total_rooms',
            'check_in_time',
            'check_out_time',
            'address',
            'city',
            'country',
            'has_wifi',
            'has_parking',
            'has_kitchen',
            'pets_allowed',
            'image',
            'is_active',
            'meals_available',
            'host_lives_on_property',
            'is_shared_with_host',
            'house_rules',
            'activities_allowed',
            'family_friendly',
            'smoking_allowed',
        ]


class HomeStayRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeStayRoom
        fields = [
            'id',
            'homestay',
            'room_name',
            'max_guest_per_room',
            'price_per_night',
            'room_utils',
            'amenities',
            'is_available',
            'has_ac',
            'has_heating',
        ]














