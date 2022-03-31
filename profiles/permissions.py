from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status
from profiles.models import User
from rest_framework import exceptions


class PagePermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action in ['list', 'create', 'update', 'retrieve']:
            return obj.owner == request.user
        elif view.action in ['retrieve']:
            return request.user.is_staff
        return False


class SubscribePermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated


class PostPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, post):
        if view.action in ['update', 'destroy']:
            return post.page.owner == request.user
        elif view.action in ['destroy']:
            return request.user.is_staff
        elif view.action in ['destroy']:
            return request.user.role == User.Roles.MODERATOR
        return False


class AdminPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action in ['block_user', 'unblock_user', 'block_page', 'unblock_page']:
            return request.user.role == User.Roles.ADMIN or request.user.role == User.Roles.MODERATOR
        return False


def check_owner_page(page, request_user):
    if page.owner != request_user:
        raise exceptions.PermissionDenied(detail="Permission denied")

