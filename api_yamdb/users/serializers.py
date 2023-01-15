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
