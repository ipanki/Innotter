from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from profiles.models import User, Page, Tag, Post


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


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'id')


class CreatePageSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Page
        fields = ('name', 'tags', 'description', 'image', 'is_private')


class ShowPageSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    followers = UserSerializer(many=True)

    class Meta:
        model = Page
        fields = ('owner', 'id', 'uuid', 'name', 'tags', 'description', 'image', 'followers', 'is_private')


class EditPageSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Page
        fields = ('name', 'tags', 'description', 'image', 'is_private')


class ShowFollowerSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    follow_requests = UserSerializer(many=True)

    class Meta:
        model = Page
        fields = ('follow_requests',)


class PageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ('owner', 'id')


class ShowPostSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('page', 'id', 'content', 'created_at', 'updated_at')


class CreatePostSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('content',)


class EditPostSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('content', 'updated_at')

