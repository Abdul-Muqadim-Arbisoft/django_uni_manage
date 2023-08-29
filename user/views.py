from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views import View
from .forms import CustomUserCreationForm, EditProfileForm
from django.shortcuts import render, redirect
from .models import CustomUser
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from .serializers import (CustomUserSerializer, CustomUserRegistrationSerializer, ChangePasswordSerializer)
from rest_framework.permissions import AllowAny


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
        return validate_and_save_form(form, request, 'login', SIGNUP_TEMPLATE, VALIDATION_ERROR_MSG)


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


class ListUsersView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]


class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                "detail": "Login Successful"
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout_api_view(request):
    logout(request)
    return Response({"detail": "Logout Successful"}, status=status.HTTP_200_OK)


class EditProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            if not request.user.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUsersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)


class CustomTokenRefreshView(TokenRefreshView):
    pass
