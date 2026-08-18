from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView

from .forms import RegistrationForm
from .models import UserProfile


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = "users/register.html"

    def form_valid(self, form):
        user = form.save()

        user.is_active = False
        user.save()

        UserProfile.objects.get_or_create(user=user)

        token = default_token_generator.make_token(user)

        verification_url = self.request.build_absolute_uri(
            reverse(
                "users:verify_email",
                kwargs={
                    "user_id": user.pk,
                    "token": token,
                },
            )
        )

        send_mail(
            subject="Подтверждение email",
            message=(
                "Здравствуйте!\n\n"
                "Вы зарегистрировались в сервисе рассылок.\n\n"
                "Для подтверждения email перейдите по ссылке:\n\n"
                f"{verification_url}\n\n"
                "Если вы не регистрировались, "
                "просто проигнорируйте это письмо."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        messages.success(
            self.request,
            "Регистрация выполнена. "
            "Проверьте email и перейдите по ссылке "
            "для подтверждения.",
        )

        return redirect("users:login")


def verify_email(request, user_id, token):
    """
    Подтверждение email пользователя.
    """

    user = get_object_or_404(
        User,
        pk=user_id,
    )

    if not default_token_generator.check_token(
        user,
        token,
    ):
        messages.error(
            request,
            "Ссылка подтверждения недействительна " "или устарела.",
        )

        return redirect("users:login")

    user.is_active = True
    user.save()

    profile, created = UserProfile.objects.get_or_create(user=user)

    profile.email_verified = True
    profile.save()

    messages.success(
        request,
        "Email успешно подтверждён! " "Теперь вы можете войти.",
    )

    return redirect("users:login")
