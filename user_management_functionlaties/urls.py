from django.urls import path
from .views import SignupView, LoginView, LogoutView, EditProfileView, ChangePasswordView, HomeView, JobListCreate

# URL patterns for the user management functionalities
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),                # URL pattern for user login
    path('signup/', SignupView.as_view(), name='signup'),              # URL pattern for user registration
    path('logout/', LogoutView.as_view(), name='logout'),              # URL pattern for user logout
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),  # URL pattern for editing user profiles
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),  # URL for changing user passwords
    path('home/', HomeView.as_view(), name='home'),                    # URL pattern for rendering the home page
    path('api/jobs/', JobListCreate.as_view(), name='job-list-create'),

]
