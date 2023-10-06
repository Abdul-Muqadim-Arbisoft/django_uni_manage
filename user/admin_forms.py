# admin_forms.py
from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm


class CustomAdminAuthenticationForm(AdminAuthenticationForm):
    username = forms.EmailField(label='Email', max_length=255)
