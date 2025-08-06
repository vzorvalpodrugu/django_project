from django.db import models
from datetime import datetime

class Master(models.Model):
    name: CharField(max_length=150, verbose_name="Имя")
    photo: ImageField(upload_to="masters/", blank=True, verbose_name="Фотография")
    phone: CharField(max_length=20, verbose_name="Телефон")
    address: CharField(max_length=255, verbose_name="Адрес")
    experience: PositiveIntegerField(verbose_name="Стаж работы", help_text="Опыт работы в годах")
    services: ManyToManyField(Service, related_name = "masters", verbose_name = "Услуги")
    is_active: BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = 'Мастера'
        ordering = ['name']

class Order(models.Model):
    client_name: CharField(max_length=100, verbose_name="Имя клиента")
    phone: CharField(max_length=20, verbose_name="Телефон")
    comment: TextField(blank=True, verbose_name="Комментарий")
    status: CharField(max_length=50, choices=STATUS_CHOICES, default="not_approved", verbose_name="Статус")
    date_created: DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_updated: DateTimeField(auto_now=True, verbose_name="Дата обновления")
    master: ForeignKey(Master, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = "Мастер")
    services: ManyToManyField(Service, related_name = "orders", verbose_name = "Услуги")
    appointment_date: DateTimeField(verbose_name="Дата и время записи")

class Service(models.Model):
    name: CharField(max_length=200, verbose_name="Название")
    description: TextField(blank=True, verbose_name="Описание")
    price: DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration: PositiveIntegerField(verbose_name="Длительность", help_text="Время выполнения в минутах")
    is_popular: BooleanField(default=False, verbose_name="Популярная услуга")
    image: ImageField(upload_to="services/", blank=True, verbose_name="Изображение")

class Review(models.Model):
    text: TextField(verbose_name="Текст отзыва")
    client_name: CharField(max_length=100, blank=True, verbose_name="Имя клиента")
    master: ForeignKey(намастера, on_delete = models.CASCADE, verbose_name = "Мастер")
    photo: ImageField(upload_to="reviews/", blank=True, null=True, verbose_name="Фотография")
    created_at: DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    rating: PositiveSmallIntegerField(MinValueValidator(1), MaxValueValidator(5), verbose_name = "Оценка")
    is_published: BooleanField(default=True, verbose_name="Опубликован")