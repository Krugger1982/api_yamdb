from django.urls import path, include
from rest_framework import routers

from .views import createuser, registration, UsersViewSet

app_name = 'users'

router_v1 = routers.DefaultRouter()
router_v1.register('users', UsersViewSet, basename='users')


urlpatterns = [
    path('v1/auth/signup/', createuser, name='signup'),
    path('v1/auth/token/', registration, name='registration'),
    path('v1/', include(router_v1.urls)),
]
