# admin_site.py
from django.contrib.admin.sites import AdminSite
from .admin_forms import CustomAdminAuthenticationForm


class CustomAdminSite(AdminSite):
    login_form = CustomAdminAuthenticationForm


# Instantiate CustomAdminSite
admin_site = CustomAdminSite(name='custom_admin')
