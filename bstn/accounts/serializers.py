# Django workflow to create api:
"""
    1. Create serializers for turning our models into json objects.
    2. Then create Viewsets so that we decide what to do when api request hit.
    3. then create routers for api endpoints.

    Runtime Order:
    Router -> ViewSet -> Serializer -> Response
"""

from rest_framework import serializers
from .models import ProviderProfile, User, GuestProfile
from django.contrib.auth import get_user_model


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'phone', 'user_type']


class GuestProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestProfile
        fields = [
            'id',
            'user',
            'name',
            'gender',
            'profile_image',
            'country',
            'city',
            'nationality',
            'preferred_language',
            'preferred_currency',
            'travel_style',
            'bio',
            'emergency_contact_name',
            'emergency_contact_number',
            'passport_number',
            'passport_expiry_date',
        ]


class ProviderProfileserializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderProfile
        fields = [
            'id',
            'display_name',
            'business_type',
            'description',
            'country',
            'city',
            'address',
            'website',
            'phone',
            'is_verified_provider',
            'kyc_status',
            'payout_method',
            'payout_details',
            'user',
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone', 'password']

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("A user with this phone already exists.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


