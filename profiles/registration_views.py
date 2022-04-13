from rest_framework.response import Response
from rest_framework import exceptions, status
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes
from profiles.presigned_url import generate_presigned_url, upload_image
from profiles.utils import login_user

from profiles.serializers import RegistrationSerializer


class RegistrationViewSet(viewsets.GenericViewSet):
    serializer_class = RegistrationSerializer

    @permission_classes([AllowAny])
    @action(detail=False, methods=['post'])
    def signup(self, request):
        user = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        image = request.FILES["image"]
        serializer = RegistrationSerializer(data={'username': user, 'email': email, 'password': password,
                                                  'image': image})
        serializer.is_valid(raise_exception=True)
        filename = upload_image(image)
        presigned_url = generate_presigned_url(filename)
        serializer.save(image_s3_path=filename)
        return Response({'data': serializer.data, 'url': presigned_url}, status=status.HTTP_201_CREATED)

    @permission_classes([AllowAny])
    @action(detail=False, methods=['post'])
    def login(self, request):
        data = login_user(request.data.get('username'), request.data.get('password'))

        return Response(data=data, status=status.HTTP_201_CREATED)
