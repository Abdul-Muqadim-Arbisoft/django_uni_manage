from django.urls import path
from .views import SignupView, LoginView, LogoutView, EditProfileView, ChangePasswordView, HomeView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('home/', HomeView.as_view(), name='home'),
]
