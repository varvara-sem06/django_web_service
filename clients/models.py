from django.conf import settings
from django.db import models


class Client(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец"
    )

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
    )

    full_name = models.CharField(
        max_length=225,
        verbose_name="ФИО",
    )

    comment = models.TextField(
        blank=True,
        verbose_name="Комментарий",
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
