from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, DateTimeRecord
from .admin_site import admin_site
from django.contrib import admin
from .models import CustomUser, DateTimeRecord


def make_active(modeladmin, request, queryset):
    """
    Set the `is_active` attribute of the selected users to True.
    """
    queryset.update(is_active=True)


make_active.short_description = "Mark selected users as active"


def make_inactive(modeladmin, request, queryset):
    """
    Set the `is_active` attribute of the selected users to False.
    """
    queryset.update(is_active=False)


make_inactive.short_description = "Mark selected users as inactive"


class CustomUserAdmin(UserAdmin):
    """
    Admin customization for the CustomUser model.

    This admin combines functionalities from two previous admin customizations:
    1. It inherits from UserAdmin for user-specific functionalities.
    2. It defines fields, filters, actions, and displays that cater to the specific attributes and requirements of CustomUser.
    """

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'description', 'father_name', 'password1', 'password2'),
        }),
    )

    fieldsets = (
        (None, {'fields': (
        'username', 'email', 'description', 'father_name', 'password', 'software_engineering_experience',
        'last_profile_update', 'is_active', 'is_staff')}),
    )

    list_display = (
    'email', 'description', 'username', 'father_name', 'first_name', 'last_name', 'software_engineering_experience',
    'last_profile_update')
    search_fields = ('email', 'first_name', 'last_name', 'father_name')
    list_filter = ('is_active', 'is_staff', 'software_engineering_experience')
    actions = [make_active, make_inactive]


admin_site.register(CustomUser, CustomUserAdmin)


class DateTimeRecordAdmin(admin.ModelAdmin):
    """
    Admin customization for the DateTimeRecord model.

    This customization defines the fields to be displayed in list view,
    fields available for search, and filters to narrow down displayed records.
    """

    list_display = ('datetime', 'converted_to_utc')
    search_fields = ('datetime',)
    list_filter = ('converted_to_utc',)


admin_site.register(DateTimeRecord, DateTimeRecordAdmin)
