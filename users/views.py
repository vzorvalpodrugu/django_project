from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login as auth_login, logout as auth_logout
from django.views.decorators.http import require_POST
from .forms import CustomAuthenticationForm, CustomUserCreationForm, CustomPasswordChangeForm
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.contrib.auth.forms import PasswordResetForm
from django.views.generic import CreateView
from django.contrib import messages

User = get_user_model()

class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    form_class = PasswordResetForm
    success_url = '/users/password-reset/done/'
    email_template_name = 'users/password_reset_email.html'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

class CustomLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = CustomAuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        messages.success(self.request, f'Добро пожаловать, {user.username}')
        return super().form_valid(form)

    def form_invalid(self, form):
        user = form.get_user()
        messages.success(self.request, f'Неверное имя пользователя или пароль.')
        return super().form_invalid(form)

class CustomPasswordChangeView(PasswordChangeView):
    template_name = "users/password_change_form.html"
    form_class = CustomPasswordChangeForm
    success_url = "/"


class CustomLogoutView(LogoutView):
    next_page = "landing"


class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = "/"

    def form_valid(self, form):
        # Сохраняем пользователя
        user = form.save()
        # Message
        messages.success(
            self.request,
            f"Добро пожаловать, {user.username}! Вы успешно зарегистрировались.",
        )
        # Выполяем авторизацию
        auth_login(self.request, user)
        # Вызываем родительский метод
        return redirect("landing")

    def form_invalid(self, form):
        # Добавляем сообщение об ошибке
        messages.error(self.request, "Пожалуйста, исправьте ошибки в форме.")
        return super().form_invalid(form)


