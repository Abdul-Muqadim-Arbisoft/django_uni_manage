# Constants related to URLs/templates paths
SIGNUP_TEMPLATE = 'user/signup.html'
LOGIN_TEMPLATE = 'user/login.html'
EDIT_PROFILE_TEMPLATE = 'user/edit_profile.html'
CHANGE_PASSWORD_TEMPLATE = 'user/change_password.html'
HOME_TEMPLATE = 'user/home.html'

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
REQUIRED_USER_FIELDS = ['father_name', 'email', 'description', 'country']
DEFAULT_SOFTWARE_ENGINEERING_EXPERIENCE = 0

# Constants related to the CustomUser forms
USER_FORM_FIELDS = (
    'email',
    'username',
    'father_name',
    'software_engineering_experience',
    'description',
    'country'

)
PASSWORD_MIN_LENGTH = 6
PASSWORD_DIGIT_MESSAGE = 'Password must contain at least 1 number.'
PASSWORD_LENGTH_MESSAGE = f'Password must be at least {PASSWORD_MIN_LENGTH} characters long.'

CREATE_PROJECT_TEMPLATE = 'project/create_project.html'
PROJECTS_LIST_TEMPLATE = 'project/projects_list.html'
VIEW_COMMENTS_TEMPLATE = 'project/view_comments.html'
SUPERVISOR_LOGIN_TEMPLATE = 'project/supervisor_login.html'
USER_DOES_NOT_EXIST_ERROR = 'User with email {email} does not exist.'
PROJECT_CREATED_SUCCESS = 'Project created successfully!'
STATUS_SUCCESS = 'success'
STATUS_KEY = 'status'
MESSAGE_KEY = 'message'
REDIRECT_URL_KEY = 'redirect_url'
DETAIL_KEY = 'detail'
ACCESS_KEY = 'access'
EMAIL_KEY = 'email'
PASSWORD_KEY = 'password'
TEXT_KEY = 'text'
COMMENT_ADDED_SUCCESS = 'Comment added successfully!'
USER_NOT_SUPERVISOR_MSG = "User is not a supervisor!"
INVALID_LOGIN_MSG = "Invalid login credentials!"

# URL patterns
API_URL = 'api/'
CREATE_PROJECT_URL = 'create_project/'
PROJECTS_LIST_URL = 'projects_list/'
VIEW_COMMENTS_URL = 'projects/<int:project_id>/comments/'
SUPERVISOR_LOGIN_URL = 'supervisor_login/'

# Router registration arguments
PROJECTS_ROUTER_ARG = r'projects'
COMMENTS_ROUTER_ARG = r'comments'
SUPERVISOR_LOGIN_ROUTER_ARG = r'supervisor_login'

# Router basenames
PROJECT_BASENAME = 'project'
COMMENT_BASENAME = 'comment'
SUPERVISOR_LOGIN_BASENAME = 'supervisor_login'

# View names
CREATE_PROJECT_NAME = 'create_project'
PROJECTS_LIST_NAME = 'projects_list'
VIEW_COMMENTS_NAME = 'view_comments'
SUPERVISOR_LOGIN_NAME = 'supervisor_login'

# Serializers field types
STUDENTS_EMAILS_FIELD = 'students_emails'
EMAIL_FIELD_TYPE = 'EmailField'
PRIMARY_KEY_FIELD_TYPE = 'PrimaryKeyRelatedField'
LIST_FIELD_TYPE = 'ListField'
MODEL_FIELD_TYPE = 'ModelSerializer'
PASSWORD_FIELD_TYPE = 'CharField'

# Field options
WRITE_ONLY_OPTION = 'write_only'
REQUIRED_OPTION = 'required'
READ_ONLY_OPTION = 'read_only'

# Fields for ProjectSerializer
ID_FIELD = 'id'
NAME_FIELD = 'name'
DESCRIPTION_FIELD = 'description'
START_DATE_FIELD = 'start_date'
END_DATE_FIELD = 'end_date'
STUDENTS_FIELD = 'students'
SUPERVISOR_FIELD = 'supervisor'

# All fields for CommentSerializer
ALL_FIELDS = '__all__'

# Validation error messages
INVALID_CREDENTIALS_ERROR = "Invalid login credentials"
NOT_A_SUPERVISOR_ERROR = "User is not a supervisor!"

# URL for the token refresh endpoint
TOKEN_REFRESH_URL = 'api/token/refresh/'

# Name for the token refresh endpoint
TOKEN_REFRESH_NAME = 'token_refresh'

COUNTRY_NAME_INDEX = 1;
