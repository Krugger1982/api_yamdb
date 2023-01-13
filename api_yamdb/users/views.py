import hashlib
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.pagination import CommonPagination
from .models import User
from .permissions import UserRoleIsAdmin, IsAdminOrProfileOwner
from .serializers import (
    RegistrationSerializer,
    UserCreationSerializer,
    UserSerializer,
    ProfileSerializer,
)


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
    serializer.is_valid(raise_exception=True)
    # значение параметра raise_exception=True автоматически сгенерит
    # ответ с кодом 400 и инфой об ошибке, если поля не прошли валидацию
    try:
        new_user = User.objects.get_or_create(**serializer.validated_data)[0]
    except IntegrityError:
        return Response('Такой пользователь или емэйл уже существуют')

    new_user.confirmation_code = generate_creation_code(new_user.username)
    new_user.save()
    send_mail(
        subject='Ваш код подтверждения',
        message=(
            f'Код для получения токена {new_user.confirmation_code}'
        ),
        from_email='administration@example.com',
        recipient_list=[new_user.email, ],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@csrf_exempt
@permission_classes([permissions.AllowAny])
def registration(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    token = RefreshToken.for_user(user)
    return Response(
        {'token': str(token.access_token)},
        status=status.HTTP_200_OK
    )


class ProfileView(APIView):
    @permission_classes([IsAdminOrProfileOwner])
    def get(self, request):
        user = self.request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes([IsAdminOrProfileOwner])
    def patch(self, request):
        user = self.request.user
        serializer = ProfileSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK
        )

    def put(self, request, *args, **kwargs):
        response = {'message': 'Метод PUT в данном эндпойнте не разрешен!'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (UserRoleIsAdmin,)
    pagination_class = CommonPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username',)

    def update(self, request, username=None):
        response = {'message': 'Метод PUT в данном эндпойнте не разрешен!'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, username=None):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                serializer.validated_data, status=status.HTTP_200_OK
            )
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
