from django.urls import path

from .views import (MessageCreateView, MessageDeleteView, MessageDetailView,
                    MessageListView, MessageUpdateView)

app_name = "messages"

urlpatterns = [
    path("", MessageListView.as_view(), name="list"),
    path("create/", MessageCreateView.as_view(), name="create"),
    path("<int:pk>/", MessageDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", MessageUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", MessageDeleteView.as_view(), name="delete"),
]
