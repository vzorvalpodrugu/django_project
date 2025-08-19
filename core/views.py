from http.client import HTTPResponse

from django.shortcuts import render
from core.data import masters, services, orders
from core.models import Master, Order, Review, Service
from django.db.models import Q
from django.shortcuts import redirect
from .forms import OrderForm, ReviewModelForm, OrderModelForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.contrib.auth.models import User
#
# user = User.objects.get(username='your_username')
# user.is_staff = True
# user.save()

class AdminStaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff and self.request.user.is_superuser

class MasterServicesView(View):
    def get(self, request):
        master_id = request.GET.get('master_id')
        try:
            master = Master.objects.get(id=master_id)
            services = master.services.all()
            services_data = [{'id': service.id, 'name': service.name} for service in services]
            return JsonResponse({'services': services_data})
        except Master.DoesNotExist:
            return JsonResponse({'error': 'Master not found'}, status=404)



class LandingView(View):
    def get(self,request):
        context = {
            'title': 'Стальная бритва',
            'masters': Master.objects.all()[:3],
            'services': Service.objects.all(),
        }
        return render(request, 'landing.html', context)

class ThanksTemplateView(TemplateView):
    template_name = 'thanks.html'

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders_list.html'
    context_object_name = 'orders'
    ordering = '-date_created'
    paginate_by = 20  # Можно добавить пагинацию

    def get_queryset(self):
        queryset = super().get_queryset()

        # Получаем параметры поиска
        q = self.request.GET.get('q', '')

        # Параметры поиска по полям
        search_by_phone = self.request.GET.get('search_by_phone') == 'true'
        search_by_name = self.request.GET.get('search_by_name') == 'true'
        search_by_comment = self.request.GET.get('search_by_comment') == 'true'

        # Поиск по текстовым полям
        if q:
            search_q = Q()
            if search_by_phone:
                search_q |= Q(phone__icontains=q)
            if search_by_name:
                search_q |= Q(client_name__icontains=q)
            if search_by_comment:
                search_q |= Q(comment__icontains=q)
            queryset = queryset.filter(search_q)

        # Фильтрация по статусам
        status_filter = Q()
        status_params = {
            'status_new': 'new',
            'status_approved': 'approved',
            'status_completed': 'completed',
            'status_cancelled': 'cancelled'
        }

        # Собираем фильтры по статусам
        applied_filters = False
        for param, status in status_params.items():
            if self.request.GET.get(param) == 'true':
                status_filter |= Q(status=status)
                applied_filters = True

        if applied_filters:
            queryset = queryset.filter(status_filter)

        # Сортировка
        order_by_date = self.request.GET.get('order_by_date', 'desc')
        if order_by_date == 'asc':
            queryset = queryset.order_by('date_created')
        else:
            queryset = queryset.order_by('-date_created')

        return queryset

class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_detail.html'
    pk_url_kwarg = 'order_id'
    context_object_name = 'order'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        print(f"Найден заказ: {obj}")
        print(f"Мастер: {obj.master}")
        print(f"Услуги: {list(obj.services.all())}")
        print(f"Дата: {obj.date_created}")

        return obj

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderModelForm
    template_name = 'order_form_class.html'
    success_url = reverse_lazy('thanks')

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Заявка на стрижку'
        context['button_text'] = "Записаться"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Заказ успешно принят.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Форма неверно заполнена!")
        return super().form_invalid(form)

class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderModelForm
    template_name = 'order_form_class.html'
    success_url = reverse_lazy('orders_list')
    pk_url_kwarg = 'order_id'

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Обновить заявку на стрижку'
        context['button_text'] = "Обновить"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Заказ обновлен.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Форма неверно заполнена!")
        return super().form_invalid(form)

class ReviewCreateView(AdminStaffRequiredMixin, CreateView):
    model = Review
    form_class = ReviewModelForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('thanks')

    def get_context_data(self, **kwargs):
        context = super(ReviewCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Оставить отзыв'
        context['button_text'] = 'Отправить отзыв'
        return context

    def form_valid(self, form):
        messages.success(self.request, "Отзыв успешно отправлен")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Форма неверно заполнена!")
        return super().form_invalid(form)

