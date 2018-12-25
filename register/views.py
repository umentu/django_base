from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.views import generic
from .forms import LoginForm
# Create your views here.


class Login(LoginView):
    """
    ログインページ
    """
    template_name = 'register/login.html'
    form_class = LoginForm


class Logout(LoginRequiredMixin, LogoutView):
    """
    ログアウトページ
    """
    template_name = 'register/login.html'
    