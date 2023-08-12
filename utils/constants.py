
# Constants related to URLs/templates paths
SIGNUP_TEMPLATE = 'user_management_functionlaties/signup.html'
LOGIN_TEMPLATE = 'user_management_functionlaties/login.html'
EDIT_PROFILE_TEMPLATE = 'user_management_functionlaties/edit_profile.html'
CHANGE_PASSWORD_TEMPLATE = 'user_management_functionlaties/change_password.html'
HOME_TEMPLATE = 'user_management_functionlaties/home.html'

# Error messages
VALIDATION_ERROR_MSG = 'Validation error occurred'
INVALID_LOGIN_CREDENTIALS_MSG = 'Invalid login credentials'

# List of view names that require authentication
PROTECTED_VIEW_NAMES = [
    'EditProfileView',
    'ChangePasswordView',
    'HomeView',
]

# Constants related to the CustomUser model
EMAIL_FIELD_NAME = 'email'
REQUIRED_USER_FIELDS = ['username', 'father_name']
DEFAULT_SOFTWARE_ENGINEERING_EXPERIENCE = 0

# Constants related to the CustomUser forms
USER_FORM_FIELDS = (
    'email',
    'username',
    'father_name',
    'software_engineering_experience',
    'description'
)
PASSWORD_MIN_LENGTH = 6
PASSWORD_DIGIT_MESSAGE = 'Password must contain at least 1 number.'
PASSWORD_LENGTH_MESSAGE = f'Password must be at least {PASSWORD_MIN_LENGTH} characters long.'
