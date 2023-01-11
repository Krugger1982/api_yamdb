from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny

from .pagination import CommonPagination
from reviews.models import (Category,
                            Title,
                            Genre,
                            Review,
                            Title
                            )
from .serializers import (
    TitleSerializer,
    CategorySerializer,
    GenreSerializer,
    CommentSerializer,
    ReviewSerializer
)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    http_method_names = ["get", "post", "patch", "delete"]
    serializer_class = TitleSerializer
    permission_classes = [AllowAny]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    http_method_names = ["get", "post", "delete"]
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ('name', )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    http_method_names = ["get", "post", "delete"]
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    filter_backends = (filters.OrderingFilter,)

    def _get_post(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self._get_post().reviews

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self._get_post())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = CommonPagination

    def _get_post(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self._get_post().comments

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, reviews=self._get_post())
