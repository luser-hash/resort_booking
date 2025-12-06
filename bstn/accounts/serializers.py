# Django workflow to create api:
"""
    1. Create serializers for turning our models into json objects.
    2. Then create Viewsets so that we decide what to do when api request hit.
    3. then create routers for api endpoints.

    Runtime Order:
    Router -> ViewSet -> Serializer -> Response
"""
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import ProviderProfile, User, GuestProfile


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


class BecomeProviderSerializer(serializers.ModelSerializer):
    """
    This serializer ensures that user doesn't already have a provider profile.
    Creats a new ProviderProfile connected to the user
    """
    class Meta:
        model = ProviderProfile
        fields = [
            'display_name',
            'business_type',
            'description',
            'country',
            'city',
            'address',
            'website',
            'phone',
        ]

        def validate(self, attrs):
            user = self.context['request'].user
            if ProviderProfile.objects.filter(user=user).exists():
                raise serializers.ValidationError('You already have a profile')
            return attrs
        
        def create(self, validated_data):
            user = self.context['request'].user
            # kyc_status default pending on model
            provider = ProviderProfile.objects.create(
                user=user,
                **validated_data
            )
            return provider


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extends JWT login response with user info (role, provider_id).
    """

    def validate(self, attrs):
        data = super().validate(attrs)  # this gives you "access" and "refresh"

        user = self.user  # the logged-in user

        # Determine role
        role = "guest"
        provider_profile = ProviderProfile.objects.filter(user=user).first()

        if user.is_staff or user.is_superuser:
            role = "admin"
        elif provider_profile:
            role = "provider"

        data["user"] = {
            "id": user.id,
            "full_name": getattr(user, "full_name", user.get_username()),
            "email": getattr(user, "email", ""),
            "role": role,
            "provider_id": provider_profile.id if provider_profile else None,
        }

        return data

