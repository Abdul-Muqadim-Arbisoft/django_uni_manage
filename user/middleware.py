from utils.helpers import redirect_if_unauthenticated


class CustomAuthenticationMiddleware:
    """
    Middleware to enforce authentication for specific view classes.

    This middleware checks if the view class handling the request is listed
    in the PROTECTED_VIEWS list. If it is, and the user is not authenticated,
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
        Check for whether the called URL is allowed to be used by a non-authenticated user.
        If not, check when the user is authenticated.
        """
        return redirect_if_unauthenticated(request, view_func.__name__)
