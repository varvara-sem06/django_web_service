from django.contrib.auth import views as auth_views
from django.urls import path

from .manager_views import ManagerUserListView, block_user, unblock_user
from .views import RegisterView, verify_email

app_name = "users"


urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "verify/<int:user_id>/<str:token>/",
        verify_email,
        name="verify_email",
    ),
    path(
        "manager/users/",
        ManagerUserListView.as_view(),
        name="manager_users",
    ),
    path(
        "manager/users/<int:pk>/block/",
        block_user,
        name="block_user",
    ),
    path(
        "manager/users/<int:pk>/unblock/",
        unblock_user,
        name="unblock_user",
    ),
]
