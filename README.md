# Univeristy PrOject Management System

A Django-based project management system that provides functionalities for project management, a supervisor can create project and add comments to it and add studetns to it along with adding descripotion of project ,Supervisor is only made through admin panel ,while there is an app named user in whihc students can make accounts as well as edit their profile update password login and signup etc and supervisor can only add the registered students opr users to the project 
## Table of Contents

- [Project Structure](#project-structure)
- [Features App Wise](#features-app-wise)
- [Management Commands](#management-commands)
- [Django Admin Enhancements](#django-admin-enhancements)
- [How to Use](#how-to-use)
- [Dependencies](#dependencies)
- [Future Enhancements](#future-enhancements)


## Project-Structure

```plaintext
muqadim_basic_user_app_django/
│
├── 📁 core/
│   ├── 📁 migrations/
│   ├── 📁 templates/
│   │   └── core/
│   │       └── home.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
│
├── 📁 project/
│   ├── 📁 migrations/
│   ├── 📁 templates/
│   │   └── project/
│   │       ├── create_project.html
│   │       ├── projects_list.html
│   │       ├── supervisor_login.html
│   │       └── view_comments.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── 📁 UniManage/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── 📁 user/
│   ├── 📁 management/
│   │   ├── 📁 commands/
│   │   │   ├── automate_terminal_commands.py
│   │   │   ├── create_dummy_pst_date_times.py
│   │   │   ├── create_multiple_users.py
│   │   │   ├── create_one_by_one_user.py
│   │   │   └── update_pst_to_utc_or_vice_versa.py
│   ├── 📁 migrations/
│   ├── 📁 templates/
│   │   └── user/
│   │       ├── change_password.html
│   │       ├── edit_profile.html
│   │       ├── home.html
│   │       ├── login.html
│   │       └── signup.html
│   ├── __init__.py
│   ├── admin.py
│   ├── admin_forms.py
│   ├── admin_site.py
│   ├── apps.py
│   ├── backends.py
│   ├── forms.py
│   ├── middleware.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── 📁 utils/
│   ├── constants.py
│   └── helpers.py
│
├── .gitignore
├── db.sqlite3
├── manage.py
└── README.md

```
# Features-App-Wise
##  Project Module

The User Management System comprises various modules. This document focuses on the **Project module**, which is designed to manage projects and their associated comments. This module incorporates both traditional web views and a RESTful API interface.

## Features

### 1. Projects

- **CRUD Operations on Projects**: Specifically for supervisors. They can perform operations like create, read, update, and delete on projects.
  
- **Project Filtering**: Projects are displayed based on the currently logged-in supervisor to ensure data privacy and relevance.

- **Student Association**: During the process of creating a project, students can be linked to it using their email addresses.

  #### Project Views
  - **Project Creation**: A template for creating new projects.
  - **Project Listing**: A template showing all projects linked with the currently logged-in supervisor.

### 2. Comments

- **CRUD Operations on Comments**: Users have the ability to add comments to projects. These comments can subsequently be read, updated, or deleted.

- **Comment Filtering**: Fetch comments based on the associated project.

  #### Comment Views
  - **View and Add Comments**: For observing and adding comments related to a specific project.

### 3. Supervisor Authentication

- **Login for Supervisors**: Provides access to supervisors for managing projects and comments.

- **JWT Token Generation**: Upon successful login, both access and refresh JWT tokens are generated for the supervisor.

- **Token Refresh**: A designated endpoint for renewing access tokens is available.

## Technical Implementation

### Models

- **Project**: Emulates individual projects, carrying attributes such as name, description, start and end dates, linked students, and the overseeing user.
- **Comment**: Represents remarks on projects. Each comment holds links to both a project and a user.

### Serializers

- **ProjectSerializer**: Takes care of the serialization and deserialization of Project entities. It contains extra operations for handling the association of students via emails during the creation of a project.
- **CommentSerializer**: Pertains to the Comment model, handling the linkage of comments to users.
- **SupervisorLoginSerializer**: Overlooks the login data of supervisors and its validation.

### Views & ViewSets

- **ProjectViewSet**: Grants CRUD operations for Project entities.
- **CommentViewSet**: Furnishes CRUD functionalities for Comment entities.
- **SupervisorLoginViewSet**: Manages the login process of supervisors and the generation of JWT tokens.

### Templates

- **CreateProjectView**: Puts forth a form for the inception of new projects.
- **ProjectsListView**: Displays all projects linked with the active supervisor session.
- **ViewCommentsView**: Portrays and oversees comments for a specified project.
- **SupervisorLoginView**: Presents the supervisor login form and controls the subsequent authentication mechanism.

## Apis


### 1. Projects API

Base Endpoint: `/api/projects/`

- **List Projects**
  - **Endpoint:** `/`
  - **Method:** `GET`
  - **Description:** Lists all the projects for the logged-in supervisor.

- **Create Project**
  - **Endpoint:** `/`
  - **Method:** `POST`
  - **Description:** Creates a new project for the logged-in supervisor.

- **Retrieve Project Details**
  - **Endpoint:** `/{project_id}/`
  - **Method:** `GET`
  - **Description:** Retrieves details of a specific project.

- **Update Project**
  - **Endpoint:** `/{project_id}/`
  - **Method:** `PUT`
  - **Description:** Updates details of a specific project.

- **Delete Project**
  - **Endpoint:** `/{project_id}/`
  - **Method:** `DELETE`
  - **Description:** Deletes a specific project.

---

### 2. Comments API

Base Endpoint: `/api/comments/`

- **List Comments**
  - **Endpoint:** `/`
  - **Method:** `GET`
  - **Description:** Lists all the comments for projects supervised by the logged-in user.

- **Create Comment**
  - **Endpoint:** `/`
  - **Method:** `POST`
  - **Description:** Creates a new comment for a specific project.

- **Retrieve Comment Details**
  - **Endpoint:** `/{comment_id}/`
  - **Method:** `GET`
  - **Description:** Retrieves details of a specific comment.

- **Update Comment**
  - **Endpoint:** `/{comment_id}/`
  - **Method:** `PUT`
  - **Description:** Updates details of a specific comment.

- **Delete Comment**
  - **Endpoint:** `/{comment_id}/`
  - **Method:** `DELETE`
  - **Description:** Deletes a specific comment.

---

### 3. Supervisor Login API

Base Endpoint: `/api/supervisor-login/`

- **Login**
  - **Endpoint:** `/`
  - **Method:** `POST`
  - **Description:** Authenticates a supervisor and issues JWT tokens.

---

### 4. Token Refresh API

- **Endpoint:** `/api/token/refresh/`
- **Method:** `POST`
- **Description:** Gets a new access token using the refresh token when the access token expires.


### URLs

The app's URL blueprint provides paths for both conventional web views and API access. It fuses with the Django Rest Framework's built-in router for handling API paths.
# User App

The User App is a Django-based application that provides both traditional form views and API views for user management.

## Features:

- User registration
- Login and Logout
- Edit profile
- Change password
- List all registered users

## Models:

- **CustomUser**: This model extends the base User model provided by Django. Fields include:
  - `username`
  - `email`
  - `father_name`
  - `description`
  - `software_engineering_experience`
  - `last_profile_update`: DateTimeField which saves the last profile update timestamp.

## APIs:

### 1. **Signup API**
- **Endpoint:** `api/signup/`
- **Method:** POST
- **Functionality:** Allows a new user to register. Required fields include `username`, `email`, `password`, `father_name`, `description`, and `software_engineering_experience`.

### 2. **Login API**
- **Endpoint:** `api/login/`
- **Method:** POST
- **Functionality:** Authenticates users and issues JWT tokens (both refresh and access tokens).

### 3. **Logout API**
- **Endpoint:** `api/logout/`
- **Method:** GET
- **Functionality:** Logs out the authenticated user.

### 4. **Edit Profile API**
- **Endpoint:** `api/edit-profile/`
- **Method:** PUT
- **Functionality:** Authenticated users can update their profile. Accepts fields like `username`, `email`, `father_name`, `description`, and `software_engineering_experience`.

### 5. **Change Password API**
- **Endpoint:** `api/change-password/`
- **Method:** PUT
- **Functionality:** Allows authenticated users to change their password. Requires the old password and the new password.

### 6. **List Users API**
- **Endpoint:** `api/list-users/`
- **Method:** GET
- **Functionality:** Fetches a list of all registered users.

### 7. **Token Refresh API**
- **Endpoint:** `api/token/refresh/`
- **Functionality:** Gets a new access token using the refresh token when the access token expires.

## Additional Components:

- **Serializers**: 
  - `CustomUserSerializer`: For listing users and editing profiles.
  - `CustomUserRegistrationSerializer`: For user registration.
  - `ChangePasswordSerializer`: For the change password functionality.

- **Authentication**:
  - Uses the `IsAuthenticated` permission class in several views, meaning only authenticated users can access them.
  - JWT (JSON Web Tokens) is used for authentication.

- **Model Backend**: The `EmailBackend` allows users to log in using their email address.

- **Middleware**: The `CustomAuthenticationMiddleware` checks for user authentication and redirects unauthenticated users to the login page.
### URLs

The app's URL blueprint provides paths for both conventional web views and API access. It fuses with the Django Rest Framework's built-in router for handling API paths.

## Management Commands

- Create DateTimeRecords: Generates DateTimeRecord objects.
- Create Random Custom Users: Generates random CustomUser objects.
- Convert Date Times: Converts date times.

## Django Admin Enhancements

Models like `CustomUser`, `DateTimeRecord`,`PROJECT`,`SUPERVISOR`,`COMMENTS` etc  are registered. Customizations include field rearrangements, list displays, and filters.

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

- **Django (Version 4.2.3)**
  
  Django is a high-level Python Web framework that encourages rapid design and clean, pragmatic design. 

- **Django Rest Framework**

  Django Rest Framework (DRF) is a powerful and flexible toolkit for building Web APIs.

- **Django Rest Framework Simple JWT**

  A JSON Web Token authentication plugin for the Django Rest Framework.

- **Djoser**

  Provides a set of Django Rest Framework views to handle basic actions such as registration, login, and password reset.

- **drf-yasg**

  Yet another Swagger generator. It's a great tool for creating API documentation with OpenAPI and Swagger.

To install all the dependencies, use the following pip command:

```bash
pip install django==4.2.3 djangorestframework django-rest-framework-simplejwt djoser drf-yasg
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
