from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.utils import timezone
from utils.constants import PROTECTED_VIEW_NAMES, DEFAULT_SOFTWARE_ENGINEERING_EXPERIENCE, PASSWORD_MIN_LENGTH, \
    PASSWORD_DIGIT_MESSAGE, PASSWORD_LENGTH_MESSAGE
from django.core.cache import cache
from django_countries import countries


def render_with_error(request, template, form, error_msg):
    """Helper function to render the template with a form and an error message."""
    return render(request, template, {'form': form, 'error': error_msg})


def validate_and_save_form(form, request, redirect_url, template, error_msg):
    """Validate the form, save if valid and redirect, else render with error."""
    if form.is_valid():
        try:
            obj = form.save()
            return redirect(redirect_url)
        except ValidationError:
            return render_with_error(request, template, form, error_msg)

    return render_with_error(request, template, form, error_msg)


def redirect_if_unauthenticated(request, view_name):
    """
    Redirects the user to the login page if trying to access a protected view without being authenticated.
    """
    if view_name in PROTECTED_VIEW_NAMES and not request.user.is_authenticated:
        return redirect('login')


def update_user_profile_fields(user):
    """
    Update custom fields for the user instance.

    If the software_engineering_experience field is not provided, it will be set to a default value,
    and the last_profile_update field will be updated with the current timestamp.
    """
    if user.software_engineering_experience is None:
        user.software_engineering_experience = DEFAULT_SOFTWARE_ENGINEERING_EXPERIENCE
    user.last_profile_update = timezone.now()


def validate_password(password):
    """
    Validate the password based on the following criteria:
    1. Length must be at least PASSWORD_MIN_LENGTH.
    2. Must contain at least 1 digit.
    """
    if len(password) < PASSWORD_MIN_LENGTH:
        raise ValidationError(PASSWORD_LENGTH_MESSAGE)
    if not any(char.isdigit() for char in password):
        raise ValidationError(PASSWORD_DIGIT_MESSAGE)
    return password


def get_countries():
    countries_list = cache.get('countries_list')

    if not countries_list:
        # This is just a sample list. Use a comprehensive one or fetch it from a source.
        countries_list = [country[1] for country in countries]
        cache.set('countries_list', countries_list, 86400)  # Cache for 24 hours

    return countries_list
