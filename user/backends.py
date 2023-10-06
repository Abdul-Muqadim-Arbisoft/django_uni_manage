from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        UserModel = get_user_model()

        # Prioritize email if provided; otherwise, use username
        lookup_value = email or username

        print(f"Trying to authenticate: {lookup_value=}, {password=}")
        try:
            if "@" in lookup_value:
                user = UserModel.objects.get(email=lookup_value)
                print("Found a user with the provided email")
            else:
                user = UserModel.objects.get(username=lookup_value)
                print("Found a user with the provided username")
        except UserModel.DoesNotExist:
            print("No user found with the provided email/username")
            return None
        else:
            if user.check_password(password):
                print("Password is correct for the user")
                return user

        print("Password is incorrect")
        return None
