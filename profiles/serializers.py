from django.contrib.auth import authenticate
from rest_framework import serializers

from profiles.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    role = serializers.CharField(read_only=True)
    image_s3_path = serializers.CharField(max_length=200, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'role', 'image_s3_path']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

