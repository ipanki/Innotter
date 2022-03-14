from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from profiles.models import User, Page, Tag


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'role', 'image_s3_path')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name',)


class CreatePageSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Page
        fields = ('name', 'tags', 'description', 'image', 'is_private')


class ShowPageSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Page
        fields = ('id', 'uuid', 'name', 'tags', 'description', 'image', 'is_private')
