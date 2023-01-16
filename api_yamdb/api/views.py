from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from reviews.models import Category, Genre, Review, Title
from .filters import TitleFilter
from .pagination import CommonPagination
from .permissions import IsAdminOrReadOnly, IsModeratorOrAuthorOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    http_method_names = ["get", "post", "patch", "delete"]
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CommonPagination
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()

    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CommonPagination
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ('name', )


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CommonPagination
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ('name', )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    filter_backends = (filters.OrderingFilter,)
    pagination_class = CommonPagination
    permission_classes = [IsModeratorOrAuthorOrReadOnly,
                          IsAuthenticatedOrReadOnly]

    def _get_post(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self._get_post().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self._get_post())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = CommonPagination
    permission_classes = [IsModeratorOrAuthorOrReadOnly,
                          IsAuthenticatedOrReadOnly]

    def _get_post(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self._get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, reviews=self._get_post())
