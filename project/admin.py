# projects/admin.py

from django import forms
from django.forms.widgets import PasswordInput
from .models import Supervisor, Project
from user.models import CustomUser
from django.contrib import admin
from user.admin_site import admin_site



class SupervisorAdminForm(forms.ModelForm):
    user_email = forms.EmailField()
    password = forms.CharField(widget=PasswordInput(), required=False)

    class Meta:
        model = Supervisor
        fields = '__all__'

    def save(self, commit=True):
        supervisor = super().save(commit=False)

        # Logic to create or find CustomUser and set it to Supervisor
        user, created = CustomUser.objects.get_or_create(email=self.cleaned_data['user_email'])
        if created or self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])
            user.save()
        supervisor.user = user

        if commit:
            supervisor.save()

        return supervisor

class SupervisorAdmin(admin.ModelAdmin):
    form = SupervisorAdminForm

admin_site.register(Supervisor, SupervisorAdmin)
admin_site.register(Project)
