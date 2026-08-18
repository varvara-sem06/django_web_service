from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from mailings.models import Recipient

from .forms import MailingForm
from .models import Mailing, MailingAttempt
from .services import send_mailing


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "newsletter/mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        return (
            Mailing.objects.filter(owner=self.request.user)
            .select_related("message")
            .prefetch_related("recipients")
        )


class MailingDetailView(LoginRequiredMixin, DetailView):

    model = Mailing
    template_name = "newsletter/mailing_detail.html"
    context_object_name = "object"

    def get_queryset(self):
        if self.request.user.is_staff:
            return Mailing.objects.all()

        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "newsletter/mailing_form.html"
    success_url = reverse_lazy("newsletter:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "newsletter/mailing_form.html"
    success_url = reverse_lazy("newsletter:list")

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "newsletter/mailing_confirm_delete.html"
    success_url = reverse_lazy("newsletter:list")

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


def start_mailing(request, pk):

    if request.method != "POST":
        return redirect(
            "newsletter:detail",
            pk=pk,
        )

    mailing = get_object_or_404(
        Mailing,
        pk=pk,
        owner=request.user,
    )

    try:
        success_count = send_mailing(mailing)

        messages.success(
            request,
            f"Рассылка выполнена. " f"Успешно отправлено: {success_count}.",
        )

    except ValueError as error:

        messages.error(
            request,
            str(error),
        )

    except Exception as error:

        messages.error(
            request,
            f"Ошибка отправки: {error}",
        )

    return redirect(
        "newsletter:detail",
        pk=mailing.pk,
    )


def disable_mailing(request, pk):
    if not request.user.is_staff:
        return redirect("home")

    mailing = get_object_or_404(
        Mailing,
        pk=pk,
    )

    mailing.is_disabled = True
    mailing.save()

    messages.success(
        request,
        "Рассылка отключена.",
    )

    return redirect(
        "newsletter:detail",
        pk=pk,
    )


@method_decorator(
    cache_page(60),
    name="dispatch",
)
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = timezone.now()

        user = self.request.user

        total_mailings = Mailing.objects.filter(owner=user).count()

        active_mailings = Mailing.objects.filter(
            owner=user,
            start_time__lte=now,
            end_time__gte=now,
        ).count()

        total_recipients = Recipient.objects.filter(owner=user).count()

        context["total_mailings"] = total_mailings
        context["active_mailings"] = active_mailings
        context["total_recipients"] = total_recipients

        return context


class StatisticsView(LoginRequiredMixin, TemplateView):
    template_name = "newsletter/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        mailings = Mailing.objects.filter(owner=user)

        attempts = MailingAttempt.objects.filter(mailing__owner=user)

        context["total_attempts"] = attempts.count()

        context["successful_attempts"] = attempts.filter(
            status=MailingAttempt.STATUS_SUCCESS
        ).count()

        context["failed_attempts"] = attempts.filter(
            status=MailingAttempt.STATUS_FAILED
        ).count()

        context["sent_messages"] = attempts.filter(
            status=MailingAttempt.STATUS_SUCCESS
        ).count()

        context["mailings"] = mailings

        return context


User = get_user_model()


@login_required
def manager_mailings(request):
    if not request.user.is_staff:
        messages.error(request, "У вас нет доступа к этой странице.")
        return redirect("home")

    mailings = (
        Mailing.objects.select_related(
            "owner",
            "message",
        )
        .prefetch_related(
            "recipients",
        )
        .order_by("-start_time")
    )

    return render(
        request,
        "newsletter/manager_mailings.html",
        {
            "mailings": mailings,
        },
    )


User = get_user_model()


@login_required
def disable_mailing(request, pk):
    if not request.user.is_staff:
        messages.error(request, "У вас нет доступа к этой странице.")
        return redirect("home")

    if request.method != "POST":
        return redirect("newsletter:manager_mailings")

    mailing = get_object_or_404(
        Mailing,
        pk=pk,
    )

    mailing.is_disabled = True
    mailing.save(update_fields=["is_disabled"])

    messages.success(request, "Рассылка отключена.")

    return redirect("newsletter:manager_mailings")


@cache_page(60 * 5)
@login_required
def statistics(request):
    """
    Статистика текущего пользователя.
    """

    user_mailings = Mailing.objects.filter(owner=request.user)

    attempts = MailingAttempt.objects.filter(mailing__owner=request.user)

    successful_attempts = attempts.filter(status=MailingAttempt.STATUS_SUCCESS).count()

    failed_attempts = attempts.filter(status=MailingAttempt.STATUS_FAILED).count()

    total_attempts = attempts.count()

    sent_messages = successful_attempts

    mailing_statistics = user_mailings.annotate(
        total_attempts=Count("attempts"),
        successful=Count(
            "attempts",
            filter=Q(attempts__status=MailingAttempt.STATUS_SUCCESS),
        ),
        failed=Count(
            "attempts",
            filter=Q(attempts__status=MailingAttempt.STATUS_FAILED),
        ),
    ).order_by("-start_time")

    return render(
        request,
        "newsletter/statistics.html",
        {
            "total_attempts": total_attempts,
            "successful_attempts": successful_attempts,
            "failed_attempts": failed_attempts,
            "sent_messages": sent_messages,
            "mailing_statistics": mailing_statistics,
        },
    )
