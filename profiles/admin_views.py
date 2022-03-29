from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from profiles.permissions import AdminPermission
import datetime

from profiles.models import Page, User


class AdminViewSet(ViewSet):
    permission_classes = (AdminPermission,)

    @action(detail=True, methods=['post'], url_path='block-user')
    def block_user(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        user.is_blocked = True
        user.save()
        return Response(status=status.HTTP_200_OK, data=f'User {user.username} blocked')

    @action(detail=True, methods=['post'], url_path='unblock-user')
    def unblock_user(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        user.is_blocked = False
        user.save()
        return Response(status=status.HTTP_200_OK, data=f'User {user.username} unblocked')

    @action(detail=True, methods=['post'], url_path='block-page')
    def block_page(self, request, pk):
        page = get_object_or_404(Page, pk=pk)
        self.check_object_permissions(request, page)
        lock_time = request.data.get('lock_time')
        page.unblock_date = datetime.datetime.utcnow() + datetime.timedelta(days=lock_time)
        page.is_blocked = True
        page.save()
        return Response(status=status.HTTP_200_OK, data=f'Page {page.name} blocked')

    @action(detail=True, methods=['post'], url_path='unblock-page')
    def unblock_page(self, request, pk):
        page = get_object_or_404(Page, pk=pk)
        self.check_object_permissions(request, page)
        page.unblock_date = datetime.datetime.utcnow() + + datetime.timedelta(days=0)
        page.is_blocked = False
        page.save()
        return Response(status=status.HTTP_200_OK, data=f'Page {page.name} unblocked')
