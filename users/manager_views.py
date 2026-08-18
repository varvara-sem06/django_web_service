from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView

from .models import UserProfile


class ManagerRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_staff:
            return redirect("home")

        return super().dispatch(
            request,
            *args,
            **kwargs,
        )


class ManagerUserListView(
    ManagerRequiredMixin,
    ListView,
):
    model = User
    template_name = "users/manager_users.html"
    context_object_name = "users"

    def get_queryset(self):
        return User.objects.select_related("profile").all()


def block_user(request, pk):

    if not request.user.is_staff:
        return redirect("home")

    if request.method != "POST":
        return redirect("users:manager_users")

    user = get_object_or_404(
        User,
        pk=pk,
    )

    if user != request.user:

        profile, created = UserProfile.objects.get_or_create(user=user)

        profile.is_blocked = True
        profile.save()

    return redirect("users:manager_users")


def unblock_user(request, pk):

    if not request.user.is_staff:
        return redirect("home")

    if request.method != "POST":
        return redirect("users:manager_users")

    user = get_object_or_404(
        User,
        pk=pk,
    )

    profile, created = UserProfile.objects.get_or_create(user=user)

    profile.is_blocked = False
    profile.save()

    return redirect("users:manager_users")
