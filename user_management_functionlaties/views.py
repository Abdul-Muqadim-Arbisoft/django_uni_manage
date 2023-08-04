"""
This module contains views for user management functionalities, including:
- User registration (SignupView)
- User login (LoginView)
- User logout (LogoutView)
- Editing user profiles (EditProfileView)
- Changing user passwords (ChangePasswordView)
- Rendering the home page (HomeView)
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.views import View
from .forms import CustomUserCreationForm, EditProfileForm


class SignupView(View):
    """View to handle user registration."""
    @staticmethod
    def get(request):
        """Render the signup form."""
        form = CustomUserCreationForm()
        return render(request, 'user_management_functionlaties/signup.html', {'form': form})

    @staticmethod
    def post(request):
        """Validate and create a new user."""
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect('home')
            except ValidationError:
                return render(request, 'user_management_functionlaties/signup.html',
                              {'form': form, 'error': 'Validation error occurred'})

        return render(request, 'user_management_functionlaties/signup.html', {'form': form})


class LoginView(View):
    """View to handle user login."""
    @staticmethod
    def get(request):
        """Render the login form."""
        return render(request, 'user_management_functionlaties/login.html')

    @staticmethod
    def post(request):
        """Authenticate and log in the user."""
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'user_management_functionlaties/login.html',
                          {'error': 'Invalid login credentials'})


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
        """Render the profile edit form."""
        form = EditProfileForm(instance=request.user)
        return render(request, 'user_management_functionlaties/edit_profile.html', {'form': form})

    @staticmethod
    def post(request):
        """Validate and update user profile."""
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            try:
                form.save()
                return redirect('home')
            except ValidationError:
                return render(request, 'user_management_functionlaties/edit_profile.html',
                              {'form': form, 'error': 'Validation error occurred'})

        return render(request, 'user_management_functionlaties/edit_profile.html', {'form': form})


class ChangePasswordView(View):
    """View to handle changing user password."""
    @staticmethod
    def get(request):
        """Render the change password form."""
        form = PasswordChangeForm(request.user)
        return render(request, 'user_management_functionlaties/change_password.html',
                      {'form': form})

    @staticmethod
    def post(request):
        """Validate and update user password."""
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            try:
                user = form.save()
                update_session_auth_hash(request, user)
                return redirect('home')
            except ValidationError:
                return render(request, 'user_management_functionlaties/change_password.html',
                              {'form': form, 'error': 'Validation error occurred'})

        return render(request, 'user_management_functionlaties/change_password.html',
                      {'form': form})


class HomeView(View):
    """View to render the home page."""
    @staticmethod
    def get(request):
        """Render the home page with the logged-in user information."""
        return render(request, 'user_management_functionlaties/home.html', {'person': request.user})
