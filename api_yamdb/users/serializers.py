from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import User


class UserCreationSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]',
        max_length=150,
    )
    email = serializers.EmailField(max_length=150)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Имя 'me' использовать как username запрещено!"
            )
        return value

# def validate(self, data):
    #     user_username = User.objects.filter(username=data['username'])
    #     user_email = User.objects.filter(email=data['email'])
    #     if user_username != user_email:
    #         # Если по отдельности существует такой username с другим емэйлом
    #         #  или на такой email зарегистрирован другой username
    #         raise serializers.ValidationError(
    #             'Пользователь с таким адресом  уже существует.',
    #             'Отправьте имеющийся у вас код подтверждения'
    #         )
    #         # в случае, если пользователь с такими (обоими!)полями существует
    #         # или в обоих переменных пустой список - проверка будет пройдена
    #     return data


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, validated_data):
        user = get_object_or_404(
            User,
            username=validated_data['username']
        )
        code = validated_data['confirmation_code']
        if code != user.confirmation_code:
            raise serializers.ValidationError(
                "Неправильное значение confirmation_code!"
            )

        return validated_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)
