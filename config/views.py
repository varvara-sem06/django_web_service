from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.cache import cache_page

from mailings.models import Recipient
from newsletter.models import Mailing


@cache_page(60 * 5)
@login_required
def home(request):
    """
    Главная страница сервиса.

    Показывает статистику текущего пользователя:
    - общее количество рассылок;
    - количество активных рассылок;
    - количество получателей.
    """

    user_mailings = Mailing.objects.filter(owner=request.user)

    user_recipients = Recipient.objects.filter(owner=request.user)

    now = timezone.now()

    total_mailings = user_mailings.count()

    active_mailings = user_mailings.filter(
        start_time__lte=now,
        end_time__gte=now,
        is_disabled=False,
    ).count()

    total_recipients = user_recipients.count()

    context = {
        "total_mailings": total_mailings,
        "active_mailings": active_mailings,
        "total_recipients": total_recipients,
    }

    return render(
        request,
        "home.html",
        context,
    )
