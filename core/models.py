from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q

class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.PositiveIntegerField(verbose_name="Длительность", help_text="Время выполнения в минутах")
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")
    image = models.ImageField(upload_to="services/", blank=True, verbose_name="Изображение")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

class Master(models.Model):
    name = models.CharField(max_length=15, verbose_name="Имя")
    photo = models.ImageField(upload_to="masters/", blank=True, verbose_name="Фотография")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=255, verbose_name="Адрес", default='somewhere')
    experience = models.PositiveIntegerField(verbose_name="Стаж работы", help_text="Опыт работы в годах", default=0)
    services = models.ManyToManyField(Service, related_name = "masters", verbose_name = "Услуги")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = 'Мастера'


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('approved', 'Подтверждён'),
        ('completed', 'Выполнена'),
        ('cancelled', 'Отменён'),
        ]

    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="Статус")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания", null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления", null=True, blank=True)
    master = models.ForeignKey(Master, on_delete = models.SET_NULL, verbose_name = "Мастер", related_name="orders", null=True, blank=True)
    services = models.ManyToManyField(Service, related_name = "orders", verbose_name = "Услуги")
    appointment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время записи")

    def __str__(self):
        return f'{self.client_name} + {self.services.name}'

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"



class Review(models.Model):
    AI_CHOICES = [
        ("ai_checked_true", "Проверено ИИ"),
        ("ai_cancelled", "Отменено ИИ"),
        ("ai_checked_in_progress", "В процессе проверки"),
        ("ai_checked_false", "Не проверено"),
    ]

    RATING_CHOICES = [
        (1, '1 - Плохо'),
        (2, '2 - Удовлетворительно'),
        (3, '3 - Хорошо'),
        (4, '4 - Очень хорошо'),
        (5, '5 - Отлично')
    ]
    text = models.TextField(verbose_name="Текст отзыва")
    client_name = models.CharField(max_length=100, blank=True, verbose_name="Имя клиента")
    master = models.ForeignKey(Master, on_delete = models.CASCADE, verbose_name = "Мастер")
    photo = models.ImageField(upload_to="reviews/", blank=True, null=True, verbose_name="Фотография")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка",
        choices=RATING_CHOICES,
    )
    is_published = models.BooleanField(default=False,
                                       verbose_name="Опубликован")

    ai_checked_status = models.CharField(
        max_length=30,
        choices=AI_CHOICES,
        default="ai_checked_false",
        verbose_name="Статус ИИ",
    )

    def __str__(self):
        return f'{self.client_name} + {self.rating}'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"