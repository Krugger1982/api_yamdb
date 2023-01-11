from django.forms import ValidationError
from rest_framework import serializers
from .models import User


class UserCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if data.get('username') == 'me':
            raise ValidationError(
                'Нельзя использовать имя "me"'
            )
        if User.objects.filter(username=data.get('username')):
            raise ValidationError(
                'Пользователь с таким именем уже существует.',
                'Отправьте имеющийся у вас код подтверждения'
            )
        if User.objects.filter(email=data.get('email')):
            raise ValidationError(
                'Пользователь с таким адресом  уже существует.',
                'Отправьте имеющийся у вас код подтверждения'
            )
        return data
