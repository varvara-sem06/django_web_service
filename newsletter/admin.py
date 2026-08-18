from django.contrib import admin

from .models import Mailing, MailingAttempt


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):

    list_display = (
        "message",
        "owner",
        "start_time",
        "end_time",
        "status",
    )

    list_filter = (
        "owner",
        "start_time",
        "end_time",
    )

    filter_horizontal = ("recipients",)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):

    list_display = (
        "mailing",
        "attempt_time",
        "status",
        "server_response",
    )

    list_filter = (
        "status",
        "attempt_time",
    )

    search_fields = ("server_response",)

    readonly_fields = ("attempt_time",)
