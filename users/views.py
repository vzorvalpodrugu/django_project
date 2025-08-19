from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login as auth_login, logout as auth_logout
from django.views.decorators.http import require_POST
from .forms import CustomAuthenticationForm, CustomUserCreationForm, \
    CustomPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetView, PasswordResetCompleteView,
)
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordResetForm
from django.views.generic import CreateView
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView
from .forms import UserProfileUpdateForm

User = get_user_model()

class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/profile_detail.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        # Пользователь может смотреть только свой профиль
        return get_object_or_404(CustomUser, pk=self.request.user.pk)


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileUpdateForm
    template_name = "users/profile_update_form.html"
    success_url = reverse_lazy("profile-detail")

    def get_object(self, queryset=None):
        # Пользователь может редактировать только свой профиль
        return get_object_or_404(CustomUser, pk=self.request.user.pk)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    form_class = CustomPasswordResetForm
    success_url = '/users/password-reset/done/'
    email_template_name = 'users/password_reset_email.html'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'

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


