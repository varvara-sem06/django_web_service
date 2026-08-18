from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
    )

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Пользователь",
    )

    email_verfiied = models.BooleanField(
        default=False,
    )

    is_blocked = models.BooleanField(
        default=False,
    )

    @property
    def is_manager(self):
        return self.user.groups.filter(name="Managers").exists()

    def __str__(self):
        return self.user.username
