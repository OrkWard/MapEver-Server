from .models import upload_file
from rest_framework import serializers

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = upload_file
        fields = '__all__'