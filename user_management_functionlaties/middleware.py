from .views import EditProfileView, ChangePasswordView, HomeView
from django.shortcuts import redirect

class CustomAuthenticationMiddleware:
    """
    Middleware to enforce authentication for specific view classes.

    This middleware checks if the view class handling the request is listed
    in the protected_views list. If it is, and the user is not authenticated,
    the user will be redirected to the login page.
    """

    def __init__(self, get_response):
        """
        Constructor for the middleware.

        :param get_response: A function to process the request and return the response.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Method to handle the request.

        :param request: The HTTP request object.
        :return: The HTTP response object.
        """
        return self.get_response(request)

    @staticmethod
    def process_view(request, view_func, view_args, view_kwargs):
        """
        Process the request before calling the view function.
        check for whether the called url is allowed to be used by non authentic user if not check when the user
        is authenticated
        """
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
