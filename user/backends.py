from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        UserModel = get_user_model()

        # Use email if it's provided; otherwise, fallback to username
        email = email or username

        print(f"Trying to authenticate: {email=}, {password=}")
        try:
            user = UserModel.objects.get(email=email)
            print("Found a user with the provided email")
        except UserModel.DoesNotExist:
            print("No user found with the provided email")
            return None
        else:
            if user.check_password(password):
                print("Password is correct for the user")
                return user

        print("Password is incorrect")
        return None
