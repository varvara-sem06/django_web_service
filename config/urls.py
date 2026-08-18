from django.contrib import admin
from django.urls import include, path

from newsletter.views import HomeView

from .views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("mailings/", include("mailings.urls")),
    path("messages/", include("messages_app.urls")),
    path("newsletter/", include("newsletter.urls")),
    path("", HomeView.as_view(), name="home"),
    path("users/", include("users.urls")),
    path("", home, name="home"),
]
