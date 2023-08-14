from django.contrib.auth.hashers import make_password

from .models import CustomUser
from rest_framework import serializers


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = CustomUser
        fields = ['id', 'username', "password", "first_name", "last_name", "email"]

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(CustomUserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(CustomUserSerializer, self).update(instance=instance, validated_data=validated_data)
