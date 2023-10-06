# Imports
from .models import Project, Comment
from .serializers import ProjectSerializer, CommentSerializer, SupervisorLoginSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from user.models import CustomUser
from django.urls import reverse
from django.views.generic import TemplateView, View
from rest_framework import viewsets, mixins
from rest_framework_simplejwt.tokens import RefreshToken

from utils.constants import *
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import AllowAny


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Project objects.
    """
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve the projects for the currently logged-in supervisor."""
        return Project.objects.filter(supervisor__user=self.request.user)

    def perform_create(self, serializer):
        """Custom creation logic to add students to a project."""
        supervisor = self.request.user.supervisor
        students_emails = serializer.validated_data.pop('students_emails', [])
        students = []
        for email in students_emails:
            try:
                student = CustomUser.objects.get(email=email)
                students.append(student)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError(USER_DOES_NOT_EXIST_ERROR.format(email=email))

        project = Project.objects.create(**serializer.validated_data, supervisor=supervisor)
        project.students.set(students)

    def create(self, request, *args, **kwargs):
        """Create a new project and handle success/error messages."""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            messages.success(request, PROJECT_CREATED_SUCCESS)
            absolute_url = request.build_absolute_uri(reverse('projects_list'))
            return Response(
                {STATUS_KEY: STATUS_SUCCESS, MESSAGE_KEY: PROJECT_CREATED_SUCCESS, REDIRECT_URL_KEY: absolute_url},
                status=status.HTTP_201_CREATED
            )
        except serializers.ValidationError as e:
            return Response({DETAIL_KEY: str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Comment objects.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve the comments of projects supervised by the currently logged-in user."""
        return Comment.objects.filter(project__supervisor__user=self.request.user)

    def perform_create(self, serializer):
        """Create a new comment and associate it with a user and a project."""
        project = get_object_or_404(Project, id=self.request.data['project'])
        serializer.save(user=self.request.user, project=project)


class SupervisorLoginViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for supervisor login functionality.
    """
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.none()
    serializer_class = SupervisorLoginSerializer

    def create(self, request, *args, **kwargs):
        """Authenticate the supervisor and generate tokens upon successful login."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(request,
                                email=serializer.validated_data[EMAIL_KEY],
                                password=serializer.validated_data[PASSWORD_KEY]
                                )
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateProjectView(TemplateView):
    """
    View for the project creation form.
    """
    template_name = CREATE_PROJECT_TEMPLATE


class ProjectsListView(TemplateView):
    """
    View to list all projects associated with the logged-in supervisor.
    """
    template_name = PROJECTS_LIST_TEMPLATE

    def get_context_data(self, **kwargs):
        """Provides context data for rendering the projects list."""
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(supervisor__user=self.request.user)
        return context


class ViewCommentsView(View):
    """
    View to display and add comments for a specific project.
    """
    template_name = VIEW_COMMENTS_TEMPLATE

    def get(self, request, *args, **kwargs):
        """Displays comments associated with a specific project."""
        project = get_object_or_404(Project, id=kwargs['project_id'])
        comments = Comment.objects.filter(project=project)
        return render(request, self.template_name, {'project': project, 'comments': comments})

    def post(self, request, *args, **kwargs):
        """Handles the addition of a new comment to a specific project."""
        project = get_object_or_404(Project, id=kwargs['project_id'])
        text = request.POST.get(TEXT_KEY)
        Comment.objects.create(user=request.user, project=project, text=text)
        messages.success(request, COMMENT_ADDED_SUCCESS)
        return redirect('view_comments', project_id=kwargs['project_id'])


class SupervisorLoginView(View):
    """
    View for the supervisor login form and logic.
    """

    template_name = SUPERVISOR_LOGIN_TEMPLATE

    def get(self, request, *args, **kwargs):
        """Renders the supervisor login form."""
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        """Handles the supervisor authentication process."""
        email = request.POST.get(EMAIL_KEY)
        password = request.POST.get(PASSWORD_KEY)
        user = authenticate(request, email=email, password=password)
        if user:
            if hasattr(user, 'supervisor'):
                login(request, user)
                return redirect('projects_list')
            else:
                return HttpResponse(USER_NOT_SUPERVISOR_MSG)
        else:
            return HttpResponse(INVALID_LOGIN_MSG)


class CustomTokenRefreshView(TokenRefreshView):
    pass
