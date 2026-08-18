from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import MessageForm
from .models import Message


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "messages_app/message_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "messages_app/message_detail.html"

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "messages_app/message_form.html"
    success_url = reverse_lazy("messages:list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "messages_app/message_form.html"
    success_url = reverse_lazy("messages:list")

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "messages_app/message_confirm_delete.html"
    success_url = reverse_lazy("messages:list")

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)
