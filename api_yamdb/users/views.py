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


def generate_creation_code_and_mail(user):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = get_random_string(20, chars)
    user.confirmation_code = hashlib.sha256(
        (secret_key + user.username).encode('utf-8')
    ).hexdigest()
    send_mail(
        subject='Ваш код подтверждения',
        message=(
            f'Код для получения токена {user.confirmation_code}'
        ),
        from_email='administration@example.com',
        recipient_list=[user.email, ],
        fail_silently=False,
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def createuser(request):
    """ Создание нового пользователя и отправка confirmation code на email,
        указанный при создании.
    """
    username = request.data.get('username')
    email = request.data.get('email')
    if not User.objects.filter(username=username, email=email).exists():
        # если пользователя с совпадением по ДВУМ полям не существует
        # то попытаемся его создать
        serializer = UserCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.create(**serializer.validated_data)
        except IntegrityError:
            return Response(
                'Такой пользователь или емэйл уже существуют',
                status=status.HTTP_400_BAD_REQUEST
            )
        response_data = serializer.validated_data
    else:
        # а если такой уже есть, то берем его из БД
        user = User.objects.get(username=username)
        response_data = request.data
    # создаем, сохраняем и отправляем пользователю код подтверждения
    generate_creation_code_and_mail(user)
    return Response(response_data, status=status.HTTP_200_OK)


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
