from django.shortcuts import render
from rest_framework import permissions, viewsets

from reviews.models import Comments, Reviews
from .serializers import CommentsSerializer, ReviewsSerializer


class ReviewsViewset(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer


class CommentsViewset(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
