# credentials_manager/serializers.py

from rest_framework import serializers
from .models import Credential

class CredentialCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = ['api_key', 'secret_key', 'unique_token','platform_type']
        read_only_fields = ['user', 'unique_token']

class CredentialRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        exclude = ['api_key', 'secret_key']
