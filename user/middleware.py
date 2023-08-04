from .views import EditProfileView, ChangePasswordView, HomeView
from django.shortcuts import redirect

class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        # List of view classes that require authentication
        protected_views = [
            EditProfileView,
            ChangePasswordView,
            HomeView,
        ]

        # Extract the class of the view function from view_func
        view_class = view_func.view_class

        # Check if the current view class is in the protected_views list
        if view_class in protected_views and not request.user.is_authenticated:
            return redirect('login')
