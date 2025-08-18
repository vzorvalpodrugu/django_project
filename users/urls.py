from django.urls import path

from .views import (
    CustomLoginView,
    CustomLogoutView,
    RegisterView,
    CustomPasswordChangeForm, CustomPasswordChangeView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view() , name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('change_password/', CustomPasswordChangeView.as_view() , name='password_change'),
]