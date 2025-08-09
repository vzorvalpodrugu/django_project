from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import landing, thanks, orders_list, order_detail, order_create, order_update


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='landing'),
    path('thanks/', thanks, name = 'thanks'),
    path('orders/', orders_list, name = 'orders_list'),
    path('orders/<int:order_id>', order_detail, name='order_detail'),
    path('orders/create/', order_create, name='order_create'),
    path('orders/update/<int:order_id>', order_update, name='order_update'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
