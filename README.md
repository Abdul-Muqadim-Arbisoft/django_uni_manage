# User Management System

A Django-based user management system that provides functionalities such as user registration, login, logout, profile editing, password changing, home page rendering, job management, and RESTful APIs for managing data.

## Table of Contents

- [Features](#features)
- [Implementation Details](#implementation-details)
- [RESTful APIs and Serialization](#restful-apis-and-serialization)
- [Management Commands](#management-commands)
- [Django Admin Enhancements](#django-admin-enhancements)
- [How to Use](#how-to-use)
- [Dependencies](#dependencies)
- [Future Enhancements](#future-enhancements)

## Features

- User Registration (SignupView): Users can register by providing their details.
- User Login (LoginView): Registered users can log in to access their accounts.
- User Logout (LogoutView): Logged-in users can log out of their accounts.
- Editing User Profiles (EditProfileView): Users can edit their profile details.
- Changing User Passwords (ChangePasswordView): Users can change their account password.
- Rendering the Home Page (HomeView): Display the home page with user information.
- Job Management (JobView): Users can post, view, and manage jobs.
- **RESTful APIs**: APIs available for user and job management functionalities.


# basic_user_app_django Project

This project provides basic user management functionalities using Django.

## 📂 Project Structure

```plaintext
basic_user_app_django/
│
├── 📁 basic_user_app_django/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── 📁 user_management_functionlaties/
│   ├── 📁 migrations/
<<<<<<< HEAD
│   ├── 📁 management/
│   │   └── 📁 commands/
│   │       └── automate_terminal_commands
│   │       └── create_dummy_pst_date_times
│   │       └── create_multiple_users.py
│   │       └── create_one_by_one_user.py
│   │       └── update_pst_to_utc_or_vice_versa.py
│   │       
=======
>>>>>>> main
│   ├── 📁 templates/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   └── views.py
│
├── 📁 utils/
│   ├── constants.py
│   └── helpers.py
│
├── .gitignore
├── manage.py
└── README.md
```
## Implementation Details

### Models

- CustomUser: Extends Django's AbstractUser with additional fields.
- DateTimeRecord: Model to store datetime records.
- Job: Represents job postings.

### Views

- SignupView: Handles user registration.
- LoginView: Authenticates and logs in the user.
- LogoutView: Logs out the user.
- EditProfileView: Allows users to edit their profile.
- ChangePasswordView: Changes user password.
- HomeView: Renders the home page.
- JobView: Manages job postings.

### Forms

- CustomUserCreationForm: For user registration.
- EditProfileForm: Edits user's profile.
- JobForm: Manages job postings.

### URL Patterns

Routes for functionalities like login, signup, logout, and more.

### Middleware

CustomAuthenticationMiddleware ensures authentication for specific view classes.

### Templates

Templates for rendering the user management views.

## RESTful APIs and Serialization

### API Views

- **UserAPI**: Fetch, update, or delete a user.
- **JobAPI**: Create, retrieve, update, or delete jobs.

### Serializers

- **UserSerializer**: Serializes and deserializes user data.
- **JobSerializer**: Serializes and deserializes job data.

## Management Commands

- Create DateTimeRecords: Generates DateTimeRecord objects.
- Create Random Custom Users: Generates random CustomUser objects.
- Convert Date Times: Converts date times.

## Django Admin Enhancements

Models like `CustomUser`, `DateTimeRecord`, and `Job` are registered. Customizations include field rearrangements, list displays, and filters.

## How to Use

1. Set up a Django project.
2. Ensure Django's authentication system is set up.
3. Include the URL patterns in your project's configuration.
4. Add the CustomAuthenticationMiddleware to the middleware list.
5. Create necessary templates for views.
6. Do install restfull api setup


## Getting Started

### 1. Clone the Repository:
```bash
git clone https://github.com/Abdul-Muqadim-Arbisoft/muqadim_basic_user_app_django.git
cd muqadim_basic_user_app_django
```

### 2. Create a virtual environment
```bash
python -m venv venv
```

### 3. Activate the virtual environment
#### For Windows:
```bash
venv\Scripts\activate
```

#### For macOS and Linux:
```bash
source venv/bin/activate
```
### 3. Run Migrations
```bash
python manage.py migrate
```
### 4.Start Development Server
```bash
python manage.py runserver
```


## Dependencies

- Django (Version 3)
- Django Rest Framework

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
