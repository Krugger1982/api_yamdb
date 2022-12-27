from rest_framework import serializers
from reviews.models import Comments, Reviews

class ReviewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reviews
        fields = '__all__'

class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = '__all__'
