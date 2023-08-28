from rest_framework import serializers
from .models import CustomUser
from utils.helpers import validate_password


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'father_name', 'description', 'software_engineering_experience', 'last_profile_update']

class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'father_name', 'description', 'software_engineering_experience']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            father_name=validated_data['father_name'],
            description=validated_data.get('description', None),
            software_engineering_experience=validated_data.get('software_engineering_experience', None)
        )
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
