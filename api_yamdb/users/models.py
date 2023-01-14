from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """ Castom model for users """
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHIOSES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    ]
    email = models.EmailField(unique=True, max_length=254, blank=False)
    role = models.CharField(max_length=10, choices=ROLE_CHIOSES, default=USER)
    bio = models.TextField(blank=True)
    password = models.CharField(max_length=128, blank=True)
    confirmation_code = models.CharField(max_length=100, blank=True)

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR or self.is_admin

    def __str__(self):
        return self.username
