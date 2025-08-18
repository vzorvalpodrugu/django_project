#
# from datetime import timedelta
# from django.utils import timezone
# from django.db.models.signals import post_save, m2m_changed
# from django.dispatch import receiver
#
# from barbershop.settings import TELEGRAM_BOT_API_KEY, TELEGRAM_USER_ID
# from .models import Review, Order
# from core.mistral import is_bad_review
# from core.telegram_bot import send_telegram_message
# import asyncio
#
#

# #
# # @receiver(post_save, sender=Order)
# # def telegram_order_notify(sender, instance, created, **kwargs):
# #     if created:
# #         # Отправляем сообщение в Telegram
# #         message = f"""
# # Новый заказ от {instance.client_name}
# # Создано в {instance.date_created.strftime('%Y-%m-%d %H:%M:%S')}
# # Телефон: {instance.phone}
# # Мастер: {instance.master.name if instance.master else 'Не указан'}
# # Услуга(и): {', '.join(service.name for service in instance.services.all())}
# # Комментарий: {instance.comment}
# # Админ-панель: http://127.0.0.1:8000/admin/core/order/{instance.id}/change/
# #
# # #заказ #{instance.master.last_name}
# # """
# #         asyncio.run(send_telegram_message(TELEGRAM_BOT_API_KEY, TELEGRAM_USER_ID, message))
#
# @receiver(m2m_changed, sender=Order.services.through)
# def telegram_order_notify(sender, instance, action, **kwargs):
#     print('сигнал m2m_changed сработал')
#     if (action == 'post_add'
#             and kwargs.get('pk_set')
#             # and timezone.now() - instance.date_created < timedelta(seconds=5)
#     ):
#         # Отправляем сообщение в Telegram
#         message = f"""
# Новый заказ от {instance.client_name}
# Создано в {instance.date_created.strftime('%Y-%m-%d %H:%M:%S')}
# Телефон: {instance.phone}
# Мастер: {instance.master.name if instance.master else 'Не указан'}
# Услуга(и): {', '.join(service.name for service in instance.services.all())}
# ---
# Комментарий: {instance.comment}
# Админ-панель: http://127.0.0.1:8000/admin/core/order/{instance.id}/change/
#
# #заказ #{instance.master.last_name}
# """
#         try:
#             run_async(send_telegram_message, TELEGRAM_BOT_API_KEY,
#                       TELEGRAM_USER_ID, message)
#         except Exception as e:
#             print(f"Ошибка при отправке: {e}")
#
#         asyncio.run(send_telegram_message(TELEGRAM_BOT_API_KEY, TELEGRAM_USER_ID, message))

from datetime import timedelta
from django.utils import timezone
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
import asyncio
import logging

from barbershop.settings import TELEGRAM_BOT_API_KEY, TELEGRAM_USER_ID
from .models import Order, Review
from core.telegram_bot import send_telegram_message
from barbershop import settings
print(f"DEBUG: TELEGRAM_BOT_API_KEY = {repr(settings.TELEGRAM_BOT_API_KEY)}")


logger = logging.getLogger(__name__)


def run_async(func, *args, **kwargs):
    """Запускает async-функцию безопасно в Django"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.ensure_future(func(*args, **kwargs))
        else:
            loop.run_until_complete(func(*args, **kwargs))
    except RuntimeError:
        asyncio.run(func(*args, **kwargs))


@receiver(m2m_changed, sender=Order.services.through)
def telegram_order_notify(sender, instance, action, pk_set, **kwargs):
    logger.debug("Сигнал m2m_changed сработал")

    # Отправляем только при добавлении услуг
    if action != 'post_add' or not pk_set:
        return

    try:
        # ✅ Убираем проверку на время для теста
        service_names = ', '.join(
            service.name for service in instance.services.filter(pk__in=pk_set)
        )

        message = f"""
Новый заказ от {instance.client_name}
Создано в {instance.date_created.strftime('%Y-%m-%d %H:%M:%S')}
Телефон: {instance.phone}
Мастер: {instance.master.name if instance.master else 'Не указан'}
Услуга(и): {service_names}
---
Комментарий: {instance.comment}
Админ-панель: http://127.0.0.1:8000/admin/core/order/{instance.id}/change/

#заказ #{instance.master.name if instance.master else 'no_master'}
"""
        asyncio.run(send_telegram_message(TELEGRAM_BOT_API_KEY, TELEGRAM_USER_ID, message))

        logger.info(f"Сообщение о заказе {instance.id} отправлено в Telegram")

    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения в Telegram: {e}", exc_info=True)


from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review


@receiver(post_save, sender=Review)
def telegram_review_notify(sender, instance, created, **kwargs):
    if not created:  # Отправляем только при создании
        return

    logger.debug("Сигнал post_save сработал для отзыва")

    try:
        message = f"""
Новый отзыв от {instance.client_name}
Создано в {instance.created_at.strftime('%Y-%m-%d %H:%M:%S')}
Мастер: {instance.master.name if instance.master else 'Не указан'}
---
Отзыв: {instance.text}
Оценка: {instance.rating}
Публикация: {instance.is_published}
Админ-панель: http://127.0.0.1:8000/admin/core/review/{instance.id}/change/

#отзыв #{instance.master.name if instance.master else 'no_master'}
"""
        asyncio.run(
            send_telegram_message(TELEGRAM_BOT_API_KEY, TELEGRAM_USER_ID,
                                  message))
        logger.info(f"Сообщение об отзыве {instance.id} отправлено в Telegram")
    except Exception as e:
        logger.error(f"Ошибка при отправке отзыва в Telegram: {e}",
                     exc_info=True)

