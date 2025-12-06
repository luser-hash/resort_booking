from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from . import models

# Register your models here.


@admin.register(models.User)
class UserAdmin(DjangoUserAdmin):
    # customize how it looks in admin
    list_display = ('username', 'email', "full_name", "phone", "user_type", "is_active", "is_staff")
    search_fields = ("username", "email", "full_name", "phone")

    # Extend the default fieldsets with extra fields
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Additional info", {
            "fields": ("full_name", "phone", "user_type", "is_email_verified", "is_phone_verified"),
        }),
    )

    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ("Additional info", {
            "classes": ("wide",),
            "fields": ("full_name", "phone", "user_type"),
        }),
    )


admin.site.register(models.GuestProfile)
admin.site.register(models.ProviderProfile)