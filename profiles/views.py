from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes

from profiles.utils import generate_access_token, generate_refresh_token, login_user

from profiles.serializers import RegistrationSerializer, CreatePageSerializer, ShowPageSerializer, EditPageSerializer, \
    ShowFollowerSerializer
from profiles.models import User, Page


class RegistrationViewSet(ViewSet):
    """
    Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    @permission_classes([AllowAny])
    @action(detail=False, methods=['post'])
    def signup(self, request):
        user = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        image_s3_path = request.data.get('image_s3_path')
        serializer = RegistrationSerializer(data={'username': user, 'email': email, 'password': password,
                                                  'image_s3_path': image_s3_path})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @permission_classes([AllowAny])
    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        data = login_user(username, password)

        return Response(data=data, status=status.HTTP_201_CREATED)


class PageViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        """List all pages"""
        pages = Page.objects.all() if request.user.is_superuser else Page.objects.filter(owner=request.user)
        serializer = ShowPageSerializer(pages, many=True)
        return Response({'data': serializer.data})

    def create(self, request):
        """Create a new page"""
        page = CreatePageSerializer(data=request.data)
        page.is_valid(raise_exception=True)
        profile = page.save(owner=request.user)
        return Response(status=status.HTTP_201_CREATED, data=CreatePageSerializer(profile).data)

    def update(self, request, pk):
        page = get_object_or_404(Page, pk=pk)
        form = EditPageSerializer(data=request.data, instance=page, partial=True)
        form.is_valid(raise_exception=True)
        profile = form.save()
        return Response(status=status.HTTP_201_CREATED, data=EditPageSerializer(profile).data)

    def retrieve(self, request, pk):
        page = get_object_or_404(Page, pk=pk)
        serializer = ShowPageSerializer(page)
        return Response({'data': serializer.data})


class SubscriptionViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk):
        page = get_object_or_404(Page, pk=pk)

        try:
            if page.is_private:
                page.follow_requests.add(request.user)
                return Response(status=status.HTTP_201_CREATED, data="Subscription request sent")
            else:
                page.followers.add(request.user)
                return Response(status=status.HTTP_201_CREATED, data="Subscribed")

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=str(e))

    @action(detail=True, methods=['get'], url_path='requests')
    def show_following_requests(self, request, pk):
        page = get_object_or_404(Page, pk=pk)
        serializer = ShowFollowerSerializer(page)
        return Response({'data': serializer.data})

    @action(detail=True, methods=['post'], url_path='accept-request')
    def accept_following_request(self, request, pk):
        """Single subscription approval"""
        page = get_object_or_404(Page, pk=pk)

        if page.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')

        if user_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='user_id is required')

        for user in page.follow_requests.all():
            if user.id == user_id:
                page.followers.add(user)
                page.follow_requests.remove(user)
                return Response(status=status.HTTP_200_OK, data='Request accepted')

        return Response(status=status.HTTP_404_NOT_FOUND, data='Request not found')

    @action(detail=True, methods=['post'], url_path='accept-requests')
    def accept_following_requests(self, request, pk):
        """Accept all subscriptions"""
        page = get_object_or_404(Page, pk=pk)

        if page.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if page.follow_requests.all() is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Requests not found')

        for user in page.follow_requests.all():
            page.followers.add(user)
            page.follow_requests.remove(user)

        return Response(status=status.HTTP_200_OK, data='Requests accepted')

