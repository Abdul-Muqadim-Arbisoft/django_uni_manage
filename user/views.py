from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views import View
from .forms import CustomUserCreationForm, EditProfileForm
from django.shortcuts import render, redirect

from utils.constants import (
    SIGNUP_TEMPLATE,
    LOGIN_TEMPLATE,
    EDIT_PROFILE_TEMPLATE,
    CHANGE_PASSWORD_TEMPLATE,
    HOME_TEMPLATE,
    VALIDATION_ERROR_MSG,
    INVALID_LOGIN_CREDENTIALS_MSG
)
from utils.helpers import (
    render_with_error,
    validate_and_save_form
)


class SignupView(View):
    """View to handle user registration."""
    @staticmethod
    def get(request):
        form = CustomUserCreationForm()
        return render(request, SIGNUP_TEMPLATE, {'form': form})

    @staticmethod
    def post(request):
        form = CustomUserCreationForm(request.POST)
        return validate_and_save_form(form, request, 'home', SIGNUP_TEMPLATE, VALIDATION_ERROR_MSG)


class LoginView(View):
    """View to handle user login."""
    @staticmethod
    def get(request):
        return render(request, LOGIN_TEMPLATE)

    @staticmethod
    def post(request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render_with_error(request, LOGIN_TEMPLATE, None, INVALID_LOGIN_CREDENTIALS_MSG)


class LogoutView(View):
    """View to handle user logout."""
    @staticmethod
    def get(request):
        """Log out the user and redirect to login."""
        logout(request)
        return redirect('login')


class EditProfileView(View):
    """View to handle editing user profile."""
    @staticmethod
    def get(request):
        form = EditProfileForm(instance=request.user)
        return render(request, EDIT_PROFILE_TEMPLATE, {'form': form})

    @staticmethod
    def post(request):
        form = EditProfileForm(request.POST, instance=request.user)
        return validate_and_save_form(form, request, 'home', EDIT_PROFILE_TEMPLATE, VALIDATION_ERROR_MSG)


class ChangePasswordView(View):
    """View to handle changing user password."""
    @staticmethod
    def get(request):
        form = PasswordChangeForm(request.user)
        return render(request, CHANGE_PASSWORD_TEMPLATE, {'form': form})

    @staticmethod
    def post(request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('home')
        else:
            return render_with_error(request, CHANGE_PASSWORD_TEMPLATE, form, VALIDATION_ERROR_MSG)


class HomeView(View):
    """View to render the home page."""
    @staticmethod
    def get(request):
        return render(request, HOME_TEMPLATE, {'person': request.user})
