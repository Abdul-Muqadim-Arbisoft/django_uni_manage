from rest_framework import serializers
from .models import Project, Comment, Supervisor
from user.models import CustomUser
from django.contrib.auth import authenticate

from utils.constants import (
    STUDENTS_EMAILS_FIELD, ID_FIELD, NAME_FIELD, DESCRIPTION_FIELD,
    START_DATE_FIELD, END_DATE_FIELD, STUDENTS_FIELD, SUPERVISOR_FIELD,
    ALL_FIELDS, INVALID_CREDENTIALS_ERROR, NOT_A_SUPERVISOR_ERROR
)


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Project model.
    Includes additional field `students_emails` to capture emails during project creation.
    """

    students_emails = serializers.ListField(
        child=serializers.EmailField(),
        write_only=True,
        required=True
    )
    students = serializers.PrimaryKeyRelatedField(many=True, queryset=CustomUser.objects.all(), required=False)
    supervisor = serializers.PrimaryKeyRelatedField(queryset=Supervisor.objects.all(), required=False)

    class Meta:
        model = Project
        fields = [ID_FIELD, NAME_FIELD, DESCRIPTION_FIELD, START_DATE_FIELD, END_DATE_FIELD,
                  STUDENTS_EMAILS_FIELD, STUDENTS_FIELD, SUPERVISOR_FIELD]


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    Includes a field to relate the comment to the user who created it.
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ALL_FIELDS


class SupervisorLoginSerializer(serializers.Serializer):
    """
    Serializer for handling supervisor login data.
    Validates if the user trying to log in is a supervisor and has valid credentials.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Ensure the provided email and password are valid and correspond to a supervisor.
        """
        user = authenticate(email=data['email'], password=data['password'])

        if not user:
            raise serializers.ValidationError(INVALID_CREDENTIALS_ERROR)

        if not hasattr(user, 'supervisor'):
            raise serializers.ValidationError(NOT_A_SUPERVISOR_ERROR)

        return data
