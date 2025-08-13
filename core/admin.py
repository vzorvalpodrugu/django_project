from django.contrib import admin
from core.models import Service, Master, Order, Review

# admin.site.register(Service)
# admin.site.register(Master)
# admin.site.register(Order)
admin.site.register(Review)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration', 'is_popular', 'price', 'masters_count']
    list_filter = ['name', 'description', 'price']
    search_fields = ['name']
    list_display_links = ['name']
    list_editable = ['is_popular', 'duration', 'price']
    actions = ['make_popular', 'make_unpopular']

    @admin.display(description='Количество мастеров')
    def masters_count(self, obj):
        return obj.masters.count()

    @admin.display(description='Сделать популярным')
    def make_popular(self, request, queryset):
        queryset.update(is_popular=True)

    @admin.display(description='Сделать непопулярным')
    def make_unpopular(self, request, queryset):
        queryset.update(is_popular=False)

class MasterAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'is_active', 'experience']
    list_filter = ['name']
    search_fields = ['name']
    list_display_links = ['name']
    list_editable = ['experience', 'is_active']
    actions = ['make_active', 'make_unactive']

    @admin.display(description='Сделать активным')
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.display(description='Сделать неактивным')
    def make_unactive(self, request, queryset):
        queryset.update(is_active=False)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'phone', 'master', 'appointment_date']
    list_filter = ['master', 'master', 'services']
    search_fields = ['client_name']
    list_display_links = ['client_name']
    list_editable = ['master']


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration', 'is_popular', 'price', 'masters_count']
    list_filter = ['name', 'description', 'price']
    search_fields = ['name']
    list_display_links = ['name']
    list_editable = ['is_popular', 'duration', 'price']
    actions = ['make_popular', 'make_unpopular']


admin.site.register(Service, ServiceAdmin)
admin.site.register(Master, MasterAdmin)
admin.site.register(Order, OrderAdmin)
