from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField, CharField
from django.contrib.auth.models import  User


class SingUp(UserCreationForm):
    email = EmailField(label='Email')
    username = CharField(label='User name')

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )