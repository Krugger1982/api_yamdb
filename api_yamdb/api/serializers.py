from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Comments, Reviews


class ReviewsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Reviews
        fields = '__all__'
        read_only_fields = ('title',)


class CommentsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ('review',)
