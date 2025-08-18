from django.urls import path

from .views import (
    CustomLoginView,
    CustomLogoutView,
    RegisterView,
    CustomPasswordChangeView,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view() , name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('password_change/', CustomPasswordChangeView.as_view() , name='password_change'),

    # Восстановление пароля
    # Шаг 2. Ввод email
    path('password-reset/', CustomPasswordResetView.as_view() , name='password_reset'),
    # Шаг 3. Вы получили инструкцию на почту
    path('password-reset/done/', CustomPasswordResetDoneView.as_view() , name='password_reset_done'),
    # Шаг 5. Ввод нового пароля
    path('password-reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # Шаг 6. Сообщение об успешном успехе
    path('password-reset/complete', CustomPasswordResetCompleteView.as_view(), name = 'password_reset_complete'),
]