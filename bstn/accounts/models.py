from django.db import models
from django_countries.fields import CountryField
from decimal import Decimal
from django.contrib.auth.models import AbstractUser

# Create your models here.

# purpose auth + identity


class User(AbstractUser):
    USER_TYPES = (
        ('NORMAL', 'Normal'),
        ('ADMIN', 'Admin'),
    )

    phone = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=50)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    # verification/ status
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

    # meta info
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name 


# Profile (Guest)
class GuestProfile(models.Model):
    TRAVEL_STYLE = (
        ('BUDGET', 'Budget'),
        ('LUXURY', 'Luxury'),
        ('ADVENTURE', 'Adventure'),
        ('FAMILY', 'Family'),
        ('SOLO', 'Solo'),
        ('BUSINESS_TRAVEL', 'Business Travel'),
        ('SHORT_BREAKS', 'Short Breaks'),
        ('CULINARY_TOURISM', 'Culinary Tourism'),
    )

    GENDER = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    )
    # relation to user, one to one means every user can have only one profile
    user = models.OneToOneField(  # OneToOne by design it's unique
        User, 
        on_delete=models.CASCADE, 
        related_name='guest_profile'
        )

    # Basic guest info
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=20, choices=GENDER)
    profile_image = models.ImageField(upload_to='profile/images', null=True, blank=True)
    country = CountryField()
    city = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50, blank=True)

    # preferences
    preferred_language = models.CharField(max_length=20,  blank=True)
    preferred_currency = models.CharField(max_length=20, blank=True)
    travel_style = models.CharField(max_length=20, choices=TRAVEL_STYLE, blank=True)
    bio = models.TextField(blank=True)

    # safety /docs 
    emergency_contact_name = models.CharField(max_length=50)
    emergency_contact_number = models.CharField(max_length=20)
    passport_number = models.CharField(max_length=100, blank=True)
    passport_expiry_date = models.DateField(null=True, blank=True)

    # meta info
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Guest:{self.name}"


# profiel (Host /  service provider)
class ProviderProfile(models.Model):
    BUSINESS_TYPE = (
        ('INDIVIDUAL', 'Individual'),
        ('COMPANY', 'Company'),
        ('AGENCY', 'Agency'),
    )

    KYC_STATUS = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    PAYOUT_METHOD = (
        ('BANK', 'Bank'),
        ('BKASH', 'Bkash'),
        ('NAGAD', 'Nagad'),
    )

    # relation to user, one to one means every user can have only one profile
    user = models.OneToOneField(  # OneToOne by design it's unique 
        User, 
        on_delete=models.CASCADE,
        related_name='provider_profile'
        )

    # business identity
    display_name = models.CharField(max_length=50)
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPE)
    description = models.TextField()

    # contact and location
    country = CountryField()
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    website = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20)

    # verification and compliance
    is_verified_provider = models.BooleanField(default=False)
    kyc_status = models.CharField(max_length=20, choices=KYC_STATUS, default='PENDING')
    kyc_document_type = models.CharField(max_length=100, blank=True)
    kyc_document_number = models.CharField(max_length=100, blank=True)
    kyc_document_file = models.FileField(upload_to='kyc/', null=True, blank=True)

    # performance / stats
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal('0.00'))
    total_reviews = models.IntegerField(default=0)
    total_bookings = models.IntegerField(default=0)

    # payout basics
    payout_method = models.CharField(max_length=20, choices=PAYOUT_METHOD, blank=True)
    payout_details = models.TextField(blank=True)

    # meta info
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Provider: {self.display_name}"