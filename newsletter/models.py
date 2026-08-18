from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from mailings.models import Recipient
from messages_app.models import Message


class Mailing(models.Model):

    STATUS_CREATED = "Создана"
    STATUS_STARTED = "Запущена"
    STATUS_FINISHED = "Завершена"

    STATUS_CHOICES = [
        (STATUS_CREATED, "Создана"),
        (STATUS_STARTED, "Запущена"),
        (STATUS_FINISHED, "Завершена"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="mailings",
    )

    start_time = models.DateTimeField(verbose_name="Дата и время начала отправки")

    end_time = models.DateTimeField(verbose_name="Дата и время окончания отправки")

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name="Сообщение",
        related_name="mailings",
    )

    recipients = models.ManyToManyField(Recipient, verbose_name="Получатели")

    is_disabled = models.BooleanField(
        default=False,
        verbose_name="Отключена менеджером",
    )

    @property
    def status(self):
        "Динамический статус рассылки"
        now = timezone.now()

        if now < self.start_time:
            return self.STATUS_CREATED

        if self.start_time <= now <= self.end_time:
            return self.STATUS_STARTED

        return self.STATUS_FINISHED

    def clean(self):
        """
        Проверка дат
        """

        if self.start_time < timezone.now():
            raise ValidationError("Дата начала рассылки не может быть в прошлом")

        if self.start_time >= self.end_time:
            raise ValidationError("Дата начала должна быть раньше даты окончания")

    def __str__(self):
        return f"{self.message.subject}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class MailingAttempt(models.Model):

    STATUS_SUCCESS = "Успешно"
    STATUS_FAILED = "Не успешно"

    STATUS_CHOICES = [
        (STATUS_SUCCESS, "Успешно"),
        (STATUS_FAILED, "Не успешно"),
    ]

    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        verbose_name="Рассылка",
        related_name="attempts",
    )

    attempt_time = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время попытки"
    )

    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, verbose_name="Статус"
    )

    server_response = models.TextField(
        blank=True, verbose_name="Ответ почтового сервера"
    )

    def __str__(self):
        return f"{self.mailing} - {self.status}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
