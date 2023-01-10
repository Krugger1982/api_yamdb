from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny

from reviews.models import Category, Title, Genre
from .serializers import (
    TitleSerializer,
    CategorySerializer,
    GenreSerializer,
)


class UsersViewSet(viewsets.ModelViewSet):
    pass


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
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass
