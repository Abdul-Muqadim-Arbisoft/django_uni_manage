from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'father_name', 'software_engineering_experience', 'description')

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        # if len(password) < 6:
        #     raise ValidationError('Password must be at least 6 characters long.')
        # if not any(char.isdigit() for char in password):
        #     raise ValidationError('Password must contain at least 1 number.')
        return password

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'father_name', 'description', 'software_engineering_experience')
