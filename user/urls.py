from django.urls import path
from .views import SignupView, LoginView, LogoutView, EditProfileView, ChangePasswordView, HomeView, ListUsersView, \
    SignupAPIView, LoginAPIView, logout_api_view, EditProfileAPIView, ChangePasswordAPIView, ListUsersAPIView
from .views import CustomTokenRefreshView

# URL patterns for the user management functionalities
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # URL pattern for user login
    path('signup/', SignupView.as_view(), name='signup'),  # URL pattern for user registration
    path('logout/', LogoutView.as_view(), name='logout'),  # URL pattern for user logout
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),  # URL pattern for editing user profiles
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),  # URL for changing user passwords
    path('home/', HomeView.as_view(), name='home'),  # URL pattern for rendering the home page
    path('api/users/', ListUsersView.as_view(), name='list-users'),

    path('api/signup/', SignupAPIView.as_view(), name='signup-api'),
    path('api/login/', LoginAPIView.as_view(), name='login-api'),
    path('api/logout/', logout_api_view, name='logout-api'),
    path('api/edit-profile/', EditProfileAPIView.as_view(), name='edit-profile-api'),
    path('api/change-password/', ChangePasswordAPIView.as_view(), name='change-password-api'),
    path('api/list-users/', ListUsersAPIView.as_view(), name='list-users-api'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

]
