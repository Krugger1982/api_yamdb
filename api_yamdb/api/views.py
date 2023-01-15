from django.shortcuts import get_object_or_404
<<<<<<< HEAD
from django_filters import rest_framework as filter_backend
from rest_framework import filters, status, viewsets
=======
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
>>>>>>> e8a486df5ff9af04395fc9353e6134c8e5a522da
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

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


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    http_method_names = ["get", "post", "delete"]
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CommonPagination
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ('name', )

    def retrieve(self, request, *args, **kwargs):
        response = {'message': 'Метод GET для объекта не разрешен!'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    http_method_names = ["get", "post", "delete"]
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CommonPagination
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ('name', )

    def retrieve(self, request, *args, **kwargs):
        response = {'message': 'Метод GET для объекта не разрешен!'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)


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
