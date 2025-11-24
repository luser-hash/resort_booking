from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Hotel)
admin.site.register(models.HomeStay)
admin.site.register(models.Resort)

# Rooms
admin.site.register(models.HotelRoom)
admin.site.register(models.ResortRoom)
admin.site.register(models.HomeStayRoom)