from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        label="Email",
    )

    first_name = forms.CharField(
        required=False,
        label="Имя",
    )

    last_name = forms.CharField(
        required=False,
        label="Фамилия",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )
