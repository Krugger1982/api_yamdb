from rest_framework import serializers

from reviews.models import Title, Category, Genre


class UserSerializer(serializers.ModelSerializer):
    pass


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(required=False, many=True)
    category = CategorySerializer(required=False)

    class Meta:
        fields = ('id', 'name', 'year',
                  'description', 'category', 'genre')
        model = Title
