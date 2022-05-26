from rest_framework import serializers
from .models import JSONFile


class JSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = JSONFile
        fields = '__all__'


class JSONDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = JSONFile
        fields = ['data']
