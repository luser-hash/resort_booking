from django.db import models
from accounts.models import ProviderProfile
from django_countries.fields import CountryField

# Hotel and Homestay model, Basestay model holds all common fields


class BaseStay(models.Model):
    class Meta:
        abstract = True

    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name='%(class)s_stays'
    )

    # Basic Info
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    total_rooms = models.IntegerField(null=False)
    check_in_time = models.TimeField()
    check_out_time = models.TimeField()

    # Location
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = CountryField()
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)

    # Amenities and Utils
    has_wifi = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    has_kitchen = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)

    # media and status
    image = models.ImageField(upload_to='hotel_stay_image/img', blank=True, null=True)
    is_active = models.BooleanField(default=False)

    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

# Extra fields for hotel


class Hotel(BaseStay):
    STAR_RATINGS = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ]
    star_rating = models.PositiveSmallIntegerField(
        choices=STAR_RATINGS,
        blank=True,
        null=True,
    )
    has_room_service = models.BooleanField(default=False)
    has_reception_24h = models.BooleanField(default=False)
    has_elevator = models.BooleanField(default=False)
    has_restaurant = models.BooleanField(default=False)
    allows_walk_in = models.BooleanField(default=False)


# Extra fields for homestay


class HomeStay(BaseStay):
    MEAL_CHOICE = [
        ('NONE', 'None'), 
        ('BREAKFAST_ONLY', 'Breakfast_only'), 
        ('HALF_BOARD', 'Half_board'), 
        ('FULL_BOARD', 'Full_board'),
    ]

    host_lives_on_property = models.BooleanField(default=False)
    is_shared_with_host = models.BooleanField(default=False)
    meals_available = models.CharField(max_length=20, choices=MEAL_CHOICE, default='NONE')
    house_rules = models.TextField(blank=True)
    activities_allowed = models.TextField(blank=True)
    family_friendly = models.BooleanField(default=False)
    smoking_allowed = models.BooleanField(default=False)

# Extra fields for resorts


class Resort(BaseStay):
    # ⭐ Star rating (fixing your Choices usage)
    STAR_RATINGS = [
        (1, "★☆☆☆☆"),
        (2, "★★☆☆☆"),
        (3, "★★★☆☆"),
        (4, "★★★★☆"),
        (5, "★★★★★"),
    ]
    star_rating = models.PositiveSmallIntegerField(
        choices=STAR_RATINGS,
        blank=True,
        null=True,
    )

    # Amenities: more extensive than a normal hotel
    num_of_pools = models.PositiveSmallIntegerField(default=0)
    has_spa = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    has_sports_center = models.BooleanField(default=False)
    has_golf_course = models.BooleanField(default=False)

    # Dining
    DINING_TYPE_CHOICES = [
        ("BASIC", "Basic dining"),
        ("MULTI_RESTAURANT", "Multiple restaurants"),
        ("LUXURY", "Luxury / fine dining focus"),
    ]
    dining_type = models.CharField(
        max_length=20,
        choices=DINING_TYPE_CHOICES,
        default="BASIC",
    )
    dining_options_count = models.PositiveSmallIntegerField(default=1)
    has_buffet = models.BooleanField(default=False)
    has_room_service = models.BooleanField(default=False)
    has_bar = models.BooleanField(default=False)

    # Activities & Entertainment
    activities_description = models.TextField(
        blank=True,
        help_text="Planned activities, events, entertainment, etc.",
    )

    # All-inclusive packages
    is_all_inclusive_available = models.BooleanField(default=False)
    all_inclusive_details = models.TextField(
        blank=True,
        help_text="What is included in all-inclusive packages.",
    )

# HotelRooms -> A Hotel can contain multiple room
# Let's create a basic common room info class


class Room(models.Model):
    class Meta:
        abstract = True 

    # Basic Info
    room_name = models.CharField(max_length=20, blank=True)
    max_guest_per_room = models.IntegerField(null=False)
    price_per_night = models.IntegerField(null=False)
    
    # utils and status
    room_utils = models.TextField(blank=True)
    amenities = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    has_ac = models.BooleanField(default=False)
    has_heating = models.BooleanField(default=False)

    @property
    def provider(self):
        # HotelRoom -> has .hotel
        if hasattr(self, 'hotel'):
            return self.hotel.provider
        
        # HomeStayRoom -> has .homestay
        if hasattr(self, 'homestay'):
            return self.homestay.provider
        
        # ResortRoom -> has .resort
        if hasattr(self, 'resort'):
            return self.resort.provider
        
        return None
    
    
class HotelRoom(Room):
    ROOM_TYPE = [
        ('SINGLE', 'Single'),
        ('DOUBLE', 'Double'),
        ('DORM', 'Dorm'),
        ('PREMIUM', 'Premium'),
    ]
    hotel = models.ForeignKey(
        Hotel, 
        on_delete=models.CASCADE, 
        related_name='hotel_rooms')
    
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE)

    def __str__(self):
        return f"{self.hotel.name} - {self.room_name}"
    

class ResortRoom(Room):
    VILLA_TYPES = [
        ('MOUNTAIN VIEW VILLA', 'Mountain View'),
        ('FARMHOUSE VILLA', 'Farmhouse Villa'),
        ('MODERN VILLA', 'Modern Villa'),
        ('BEACHFRONT VILLA', 'Beachfront Villa'),
        ('INFINITY POOL VILLA', 'Infinity Pool Villa'),
        ('COUPLE VILLA', 'Couple Ville'),
        ('PRESIDENTIAL SUITE', 'Presidential Suite'),
    ]
    resort = models.ForeignKey(
        Resort, 
        on_delete=models.CASCADE, 
        related_name='resort_rooms')
    
    villa_type = models.CharField(max_length=30, choices=VILLA_TYPES)

    def __str__(self):
        return f"{self.resort.name} - {self.room_name}"
    

class HomeStayRoom(Room):
    homestay = models.ForeignKey(
        HomeStay, 
        on_delete=models.CASCADE, 
        related_name='homestay_rooms')

    def __str__(self):
        return f"{self.homestay.name} - {self.room_name}"