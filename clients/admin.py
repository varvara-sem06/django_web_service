from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "email",
        "owner",
    )

    search_fields = (
        "full_name",
        "email",
    )
