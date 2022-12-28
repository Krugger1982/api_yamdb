from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets

from reviews.models import Comments, Reviews, Title
from .serializers import CommentsSerializer, ReviewsSerializer


class ReviewsViewset(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer

    def _get_post(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self._get_post().reviews

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self._get_post())


class CommentsViewset(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

    def _get_post(self):
        return get_object_or_404(Reviews, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self._get_post().comments

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, reviews=self._get_post())
