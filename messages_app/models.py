from django.conf import settings
from django.db import models


class Message(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
    )

    subject = models.CharField(
        max_length=225,
        verbose_name="Тема письма",
    )

    body = models.TextField(
        verbose_name="Тело письма",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Датат создания",
    )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
