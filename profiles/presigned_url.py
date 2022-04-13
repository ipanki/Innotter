import boto3
from typing import Optional
from botocore.exceptions import ClientError
import uuid
import os
import magic
from rest_framework.exceptions import ValidationError

from Innotter import settings


def _file_extension_check(image):
    content_type = magic.from_buffer(image.read(), mime=True)
    image.seek(0)
    if not content_type.startswith('image/'):
        raise ValidationError("File is not an image.")


def upload_image(image):
    _file_extension_check(image)
    _, ext = os.path.splitext(f'{image}')
    filename = str(uuid.uuid4()) + ext
    s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    obj = s3.Object('django-innotter', filename)
    obj.put(Body=image, Key=filename, ContentType=image.content_type)
    return filename


def generate_presigned_url(filename):
    bucket_name = 'django-innotter'
    bucket_resource_url = filename
    url = _create_presigned_url(
        bucket_name,
        bucket_resource_url
    )
    return url


def _create_presigned_url(bucket_name: str, object_name: str, expiration=3600) -> Optional[str]:

    s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    response = s3_client.generate_presigned_url('get_object',
                                                Params={'Bucket': bucket_name, 'Key': object_name},
                                                ExpiresIn=expiration)
    return response
