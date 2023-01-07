from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import path
from .views import createuser


app_name = 'users'

urlpatterns = [
    path('v1/auth/signup/', createuser, name='signup'),
    path(
        'v1/auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
]
