from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """ Castom model for users """
    USER = 'User'
    MODERATOR = 'Moderator'
    ADMIN = 'Admin'
    ROLE_CHIOSES = [
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin')
    ]
    email = models.EmailField(unique=True, max_length=254, blank=False)
    role = models.CharField(max_length=10, choices=ROLE_CHIOSES, default=USER)
    bio = models.TextField(blank=True)
    confirmation_code = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username
