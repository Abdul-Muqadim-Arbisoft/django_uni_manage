from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating a new CustomUser.

    This form inherits from Django's built-in UserCreationForm, and it includes
    additional fields such as email, username, father's name, software engineering experience,
    and description. The password must be at least 6 characters long and include at least 1 number.
    """

    class Meta:
        model = CustomUser                     # Model associated with the form
        fields = ('email',
                  'username',
                  'father_name',
                  'software_engineering_experience',
                  'description'
                  )  # Fields included in the form

    def clean_password1(self):
        """Custom validation for the password1 field."""
        password = self.cleaned_data.get('password1')
        if len(password) < 6:
            raise ValidationError('Password must be at least 6 characters long.')  # Password length check
        if not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain at least 1 number.')  # Password digit check
        return password


class EditProfileForm(forms.ModelForm):
    """
    Form for editing a CustomUser's profile.

    This form allows a user to edit their email, username, father's name, description,
    and software engineering experience. It is based on Django's ModelForm class and
    uses the CustomUser model.
    """

    class Meta:
        model = CustomUser  # Model associated with the form
        fields = ('email',
                  'username',
                  'father_name',
                  'description',
                  'software_engineering_experience'
                  )  # Fields included in the form
