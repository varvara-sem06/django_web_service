from django.urls import path

from .views import (MailingCreateView, MailingDeleteView, MailingDetailView,
                    MailingListView, MailingUpdateView, StatisticsView,
                    disable_mailing, manager_mailings, start_mailing,
                    statistics)

app_name = "newsletter"

urlpatterns = [
    path("", MailingListView.as_view(), name="list"),
    path("create/", MailingCreateView.as_view(), name="create"),
    path("<int:pk>/", MailingDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", MailingUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", MailingDeleteView.as_view(), name="delete"),
    path("<int:pk>/send/", start_mailing, name="send"),
    path("<int:pk>/disable/", disable_mailing, name="disable"),
    path("statistics/", StatisticsView.as_view(), name="statistics"),
    path("manager/", manager_mailings, name="manager_mailings"),
    path(
        "statistics/",
        statistics,
        name="statistics",
    ),
]
