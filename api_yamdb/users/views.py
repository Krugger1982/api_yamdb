import hashlib
from http import HTTPStatus
from rest_framework.decorators import api_view, permission_classes
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import permissions
from rest_framework.response import Response

from .models import User
from .serializers import UserCreationSerializer


def generate_creation_code(username):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = get_random_string(20, chars)
    return hashlib.sha256((secret_key + username).encode('utf-8')).hexdigest()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def createuser(request):
    """ Создание нового пользователя и отправка confirmation code на email,
        указанный при создании.
    """
    serializer = UserCreationSerializer(data=request.data)
    # Если в запросе переданы правильные значения полей,
    # создается (берется из базы) пользователь
    if serializer.is_valid(raise_exception=True):
        # значение параметра raise_exception=True автоматически сгенерит
        # ответ с кодом 400 и инфой об ошибке, если поля не прошли валидацию
        new_user = User.objects.get_or_create(**serializer.validated_data)[0]
        new_user.confirmation_code = generate_creation_code(new_user.username)
        send_mail(
            subject='Ваш код подтверждения',
            message=(
                f'Отправьте этот код для получения токена {new_user.confirmation_code}'
            ),
            from_email='administration@example.com',
            recipient_list=[new_user.email, ],
            fail_silently=False,
        )
        new_user.save()
        return Response(serializer.data, status=HTTPStatus.OK)
