from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import (
    LandingView,
    ThanksTemplateView,
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderUpdateView,
    ReviewCreateView,
    MasterServicesView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ajax/get-master-services/', MasterServicesView.as_view(), name = 'get_master_services'),
    path('ajax/thanks',ThanksTemplateView.as_view()),
    path('', LandingView.as_view(), name='landing'),
    path('thanks/', ThanksTemplateView.as_view(), name = 'thanks'),
    path('orders/', OrderListView.as_view(), name = 'orders_list'),
    path('orders/<int:order_id>', OrderDetailView.as_view(), name='order_detail'),
    path('orders/create/', OrderCreateView.as_view(), name='order_create'),
    path('orders/update/<int:order_id>', OrderUpdateView.as_view(), name='order_update'),
    path('reviews/create/', ReviewCreateView.as_view(), name='reviews_create'),

    # Пользователи
    path('users/', include('users.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
