from django import forms

from mailings.models import Recipient
from messages_app.models import Message

from .models import Mailing


class MailingForm(forms.ModelForm):

    class Meta:
        model = Mailing

        fields = (
            "start_time",
            "end_time",
            "message",
            "recipients",
        )

        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "recipients": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        if user:
            self.fields["message"].queryset = Message.objects.filter(owner=user)

            self.fields["recipients"].queryset = Recipient.objects.filter(owner=user)
