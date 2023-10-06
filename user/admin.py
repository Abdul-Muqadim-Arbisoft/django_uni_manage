from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .admin_site import admin_site


class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email','description', 'father_name', 'password1', 'password2'),  # include other fields of CustomUser
        }),
    )
    fieldsets = (
        (None, {'fields': ('username','email','description', 'father_name','password')}),  # include other fields of CustomUser
    )
    list_display = ('email', 'description','username','father_name')  # display fields in the user list page


admin_site.register(CustomUser, CustomUserAdmin)
