from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .form_sing_up import SingUp as SingUpForm


class SingUp(CreateView):
    model = User
    form_class = SingUpForm
    template_name = 'registration\sig_up.html'
    success_url = '/articles/'