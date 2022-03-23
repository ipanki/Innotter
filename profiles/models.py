import uuid as uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=Roles.choices, default=Roles.USER)
    title = models.CharField(max_length=80)

    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return f'Name={self.username}'


class Tag(models.Model):
    name = models.CharField(max_length=30)


class Page(models.Model):
    name = models.CharField(max_length=80)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    description = models.TextField()
    tags = models.ManyToManyField('profiles.Tag', related_name='pages')

    owner = models.ForeignKey('profiles.User', on_delete=models.CASCADE, related_name='pages')
    followers = models.ManyToManyField('profiles.User', related_name='followed_pages')

    image = models.URLField(null=True, blank=True)

    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField('profiles.User', related_name='follow_requests')

    unblock_date = models.DateTimeField(null=True, blank=True)


class Post(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=180)

    reply_to = models.ForeignKey('profiles.Post', on_delete=models.SET_NULL, null=True, related_name='replies')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
