from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login as auth_login, logout as auth_logout
from django.views.decorators.http import require_POST
from .forms import CustomAuthenticationForm, CustomUserCreationForm, CustomPasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import CreateView
from django.contrib import messages

User = get_user_model()

# def register(request):
#     if request.method == "POST":
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = User.objects.create_user(
#                 username=form.cleaned_data["username"],
#                 email=form.cleaned_data["email"],
#                 password=form.cleaned_data["password"],
#             )
#             auth_login(request, user)
#             return redirect("landing")
#     else:
#         form = RegistrationForm()
#     return render(request, "users/register.html", {"form": form})

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
    template_name = "users/change_password.html"
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


