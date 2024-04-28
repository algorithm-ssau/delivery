from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='E-mail',
        max_length=settings.LIMIT_CHAR_254,
        unique=True
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=settings.LIMIT_CHAR_150
    )
    first_name = models.CharField(
        verbose_name='Логин',
        max_length=settings.LIMIT_CHAR_150,
        unique=True
    )
