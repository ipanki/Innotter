from rest_framework.response import Response
from rest_framework import exceptions, status
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes

from profiles.utils import login_user

from profiles.serializers import RegistrationSerializer


class RegistrationViewSet(viewsets.GenericViewSet):
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
