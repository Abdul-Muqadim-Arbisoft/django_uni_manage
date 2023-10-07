from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from utils.constants import USER_FORM_FIELDS
from utils.helpers import validate_password, get_countries


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating a new CustomUser.

    This form inherits from Django's built-in UserCreationForm and adds
    additional fields for the CustomUser.
    """
    country = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        countries = get_countries()
        self.fields['country'].choices = [(country, country) for country in countries]

    class Meta:
        model = CustomUser
        fields = USER_FORM_FIELDS

    def clean_password1(self):
        """Custom validation for the password1 field."""
        password = self.cleaned_data.get('password1')
        return validate_password(password)


class EditProfileForm(forms.ModelForm):
    """
    Form for editing a CustomUser's profile.

    This form uses the CustomUser model.
    """

    class Meta:
        model = CustomUser
        fields = USER_FORM_FIELDS
