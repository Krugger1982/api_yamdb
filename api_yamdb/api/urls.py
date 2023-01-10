from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import (
    CategoryViewSet,
    TitleViewSet,
    GenreViewSet,
    ReviewViewSet,
    CommentViewSet,
    UsersViewSet,
)

app_name = 'api'


router_v1 = routers.DefaultRouter()

router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'users', UsersViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
