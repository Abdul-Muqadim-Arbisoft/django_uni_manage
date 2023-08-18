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


class CustomUserAdmin(admin.ModelAdmin):
    """
    Admin customization for the CustomUser model.
    Defines the fields to be displayed in list view, search fields, filters, and available actions.
    """
    list_display = ('email', 'first_name', 'last_name',
                    'father_name', 'software_engineering_experience', 'last_profile_update'
                    )
    search_fields = ('email', 'first_name', 'last_name', 'father_name')
    list_filter = ('is_active', 'is_staff', 'software_engineering_experience')
    fields = ('email', 'father_name', 'first_name',
              'last_name', 'description', 'software_engineering_experience',
              'last_profile_update', 'is_active', 'is_staff'
              )
    actions = [make_active, make_inactive]


admin.site.register(CustomUser, CustomUserAdmin)


class DateTimeRecordAdmin(admin.ModelAdmin):
    """
    Admin customization for the DateTimeRecord model.
    Defines the fields to be displayed in list view, search fields, and filters.
    """
    list_display = ('datetime', 'converted_to_utc')
    search_fields = ('datetime',)
    list_filter = ('converted_to_utc',)


admin.site.register(DateTimeRecord, DateTimeRecordAdmin)
