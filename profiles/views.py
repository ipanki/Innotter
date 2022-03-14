from rest_framework.response import Response
from rest_framework import exceptions, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes

from profiles.utils import generate_access_token, generate_refresh_token, login_user

from profiles.serializers import RegistrationSerializer, CreatePageSerializer, ShowPageSerializer
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
        serializer = RegistrationSerializer(data={'username': user, 'email': email, 'password' : password,
                                                  'image_s3_path' : image_s3_path})
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

    def list(self, request):
        """List all issues"""
        issues = Page.objects.all()
        serializer = ShowPageSerializer(issues, many=True)
        return Response({'data': serializer.data})

    @permission_classes([IsAuthenticated])
    def create(self, request):
        """Create a new page"""
        page = CreatePageSerializer(data=request.data)
        page.is_valid(raise_exception=True)
        profile = page.save(owner=request.user)
        return Response(status=status.HTTP_201_CREATED, data=CreatePageSerializer(profile).data)



