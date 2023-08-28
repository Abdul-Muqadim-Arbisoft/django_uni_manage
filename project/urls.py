from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ProjectViewSet, CommentViewSet, CreateProjectView,
                    ProjectsListView, ViewCommentsView, SupervisorLoginView, SupervisorLoginViewSet,
                    CustomTokenRefreshView
                    )
from utils.constants import (API_URL, CREATE_PROJECT_URL, PROJECTS_LIST_URL,
                             VIEW_COMMENTS_URL, SUPERVISOR_LOGIN_URL,
                             PROJECTS_ROUTER_ARG, COMMENTS_ROUTER_ARG, SUPERVISOR_LOGIN_ROUTER_ARG,
                             PROJECT_BASENAME, COMMENT_BASENAME, SUPERVISOR_LOGIN_BASENAME,
                             CREATE_PROJECT_NAME, PROJECTS_LIST_NAME, VIEW_COMMENTS_NAME, SUPERVISOR_LOGIN_NAME,
                             TOKEN_REFRESH_URL,TOKEN_REFRESH_NAME,
                             )
from rest_framework_simplejwt.views import TokenRefreshView

# Configure the router to use the ViewSets
router = DefaultRouter()
router.register(PROJECTS_ROUTER_ARG, ProjectViewSet, basename=PROJECT_BASENAME)
router.register(COMMENTS_ROUTER_ARG, CommentViewSet, basename=COMMENT_BASENAME)
router.register(SUPERVISOR_LOGIN_ROUTER_ARG, SupervisorLoginViewSet, basename=SUPERVISOR_LOGIN_BASENAME)

# Define URL patterns
urlpatterns = [
    # API routes defined through DRF router
    path(API_URL, include(router.urls)),

    # Route for project creation
    path(CREATE_PROJECT_URL, CreateProjectView.as_view(), name=CREATE_PROJECT_NAME),

    # Route for listing projects associated with the logged-in supervisor
    path(PROJECTS_LIST_URL, ProjectsListView.as_view(), name=PROJECTS_LIST_NAME),

    # Route for viewing and adding comments to a specific project
    path(VIEW_COMMENTS_URL, ViewCommentsView.as_view(), name=VIEW_COMMENTS_NAME),

    # Route for the supervisor login form and authentication process
    path(SUPERVISOR_LOGIN_URL, SupervisorLoginView.as_view(), name=SUPERVISOR_LOGIN_NAME),

    path(TOKEN_REFRESH_URL, CustomTokenRefreshView.as_view(), name=TOKEN_REFRESH_NAME),
]
