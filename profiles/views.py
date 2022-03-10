from rest_framework.response import Response
from rest_framework import exceptions, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes

from profiles.utils import generate_access_token, generate_refresh_token

from .serializers import RegistrationSerializer
from profiles.models import User


class RegistrationViewSet(ViewSet):
    """
    Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        user = request.data.get('user', {})
        serializer = RegistrationSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if (username is None) or (password is None):
            raise exceptions.AuthenticationFailed(
                'username and password required')

        user = User.objects.filter(username=username).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Wrong password')

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        data = {
            'access_token': access_token,
            'user': user.id,
            'refresh_token' : refresh_token,
        }

        return Response(data=data, status=status.HTTP_201_CREATED)



