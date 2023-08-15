from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    """
    Serializer for processing the job data
    """
    class Meta:
        model = Job
        fields = '__all__'
