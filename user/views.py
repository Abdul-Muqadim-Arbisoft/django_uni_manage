from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.views import View
from .forms import CustomUserCreationForm, EditProfileForm
from .models import CustomUser

class SignupView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'user_management_functionlaties/signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect('home')
            except ValidationError:
                return render(request, 'user_management_functionlaties/signup.html', {'form': form, 'error': 'Validation error occurred'})

        return render(request, 'user_management_functionlaties/signup.html', {'form': form})

class LoginView(View):
    def get(self, request):
        return render(request, 'user_management_functionlaties/login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'user_management_functionlaties/login.html', {'error': 'Invalid login credentials'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = EditProfileForm(instance=request.user)
        return render(request, 'user_management_functionlaties/edit_profile.html', {'form': form})

    def post(self, request):
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            try:
                form.save()
                return redirect('home')
            except ValidationError:
                return render(request, 'user_management_functionlaties/edit_profile.html', {'form': form, 'error': 'Validation error occurred'})

        return render(request, 'user_management_functionlaties/edit_profile.html', {'form': form})

class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, 'user_management_functionlaties/change_password.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            try:
                user = form.save()
                update_session_auth_hash(request, user)
                return redirect('home')
            except ValidationError:
                return render(request, 'user_management_functionlaties/change_password.html', {'form': form, 'error': 'Validation error occurred'})

        return render(request, 'user_management_functionlaties/change_password.html', {'form': form})


class HomeView(View):
    def get(self, request):
        return render(request, 'user_management_functionlaties/home.html', {'user': request.user})
