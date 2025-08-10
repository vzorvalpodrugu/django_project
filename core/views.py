from http.client import HTTPResponse

from django.shortcuts import render
from core.data import masters, services, orders
from core.models import Master, Order, Review
from django.db.models import Q
from django.shortcuts import redirect
from .forms import OrderForm, ReviewModelForm
from django.http import JsonResponse

# from django.contrib.auth.models import User
#
# user = User.objects.get(username='your_username')
# user.is_staff = True
# user.save()

def get_master_services(request):
    master_id = request.GET.get('master_id')
    try:
        master = Master.objects.get(id=master_id)
        services = master.services.all()
        services_data = [{'id': service.id, 'name': service.name} for service in services]
        return JsonResponse({'services' : services_data})
    except Master.DoesNotExist:
        return JsonResponse({'error': 'Master not found'}, status=404)

def landing(request):
    masters_db = Master.objects.all()
    reviews_db = Review.objects.all()
    context = {
        "masters": masters_db,
        "reviews": reviews_db,
        "title": "Барбершоп 'Стальная Борода'",
        "services": services
    }
    return render(request, 'landing.html', context)

def thanks(request):
    context = {
        "text" : "Заявка принята!"
    }
    return render(request, 'thanks.html', context)


def orders_list(request):
    # Получаем параметры поиска
    q = request.GET.get('q', '')

    # Параметры поиска по полям
    search_by_phone = request.GET.get('search_by_phone') == 'true'
    search_by_name = request.GET.get('search_by_name') == 'true'
    search_by_comment = request.GET.get('search_by_comment') == 'true'

    # Параметры сортировки
    order_by_date = request.GET.get('order_by_date', 'desc')

    # Начальный запрос
    query = Order.objects.all()

    # Поиск по текстовым полям
    if q:
        search_q = Q()
        if search_by_phone:
            search_q |= Q(phone__icontains=q)
        if search_by_name:
            search_q |= Q(client_name__icontains=q)
        if search_by_comment:
            search_q |= Q(comment__icontains=q)
        query = query.filter(search_q)

    # Фильтрация по статусам
    status_filter = Q()
    if request.GET.get('status_new') == 'true':
        status_filter |= Q(status='new')
    if request.GET.get('status_approved') == 'true':
        status_filter |= Q(status='approved')
    if request.GET.get('status_completed') == 'true':
        status_filter |= Q(status='completed')
    if request.GET.get('status_cancelled') == 'true':
        status_filter |= Q(status='cancelled')

    # Применяем фильтр только если выбран хотя бы один статус
    if any([
        request.GET.get('status_new') == 'true',
        request.GET.get('status_approved') == 'true',
        request.GET.get('status_completed') == 'true',
        request.GET.get('status_cancelled') == 'true'
    ]):
        query = query.filter(status_filter)

    # Сортировка
    order_field = '-date_created' if order_by_date == 'desc' else 'date_created'
    query = query.order_by(order_field)

    context = {
        'orders': query,
        'title': 'Список заявок',
        'current_q': q,
        'search_params': {
            'by_phone': search_by_phone,
            'by_name': search_by_name,
            'by_comment': search_by_comment,
        },
        'status_new': request.GET.get('status_new') == 'true',
        'status_approved': request.GET.get('status_approved') == 'true',
        'status_completed': request.GET.get('status_completed') == 'true',
        'status_cancelled': request.GET.get('status_cancelled') == 'true',
        'order_by': order_by_date
    }

    return render(request, 'orders_list.html', context)

def order_detail(request, order_id):
    try:
        order = [order for order in orders if order['id'] == order_id][0]
    except IndexError:
        return render(request, '404.html', status=404)

    context = {
        "order": order
    }
    return render(request, 'order_detail.html', context)

def order_create(request):
    if request.method == 'GET':
        form = OrderForm()
        context = {
            "title": "Заявка на стрижку",
            'button_text': "Записаться",
            "form": form,
        }
        return render(request, 'order_form_class.html', context)

    elif request.method == 'POST':
        form = OrderForm(request.POST)
        if not form.is_valid():
            context = {
                'title': 'Заявка на стрижку',
                'button_text' : "Записаться",
                'form': form,
            }
            return render(request, 'order_form_class.html', context)

        client_name = request.POST['client_name']
        phone = request.POST['phone']
        comment = request.POST['comment']

        if not client_name or not phone:
            return render(request, 'order_form.html')

        order = Order.objects.create(
            client_name = form.cleaned_data['client_name'],
            phone = form.cleaned_data['phone'],
            comment = form.cleaned_data['comment'],
            master = form.cleaned_data.get('master'),
        )
        order.services.set(form.cleaned_data['services'])
        return redirect(thanks)

def order_update(request, order_id):
    if request.method == 'GET':
        try:
            order: Order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return HTTPResponse("Заявка не найдена", status=404)

        initial = {
            'client_name': order.client_name,
            'phone': order.phone,
            'comment': order.comment,
            'master': order.master,
            "services": order.services.all()
        }
        form = OrderForm(initial=initial)

        context = {
            "title": "Редактирование заявки",
            'button_text': "Сохранить",
            "order": order,
            "form": form,
        }

        return render(request, 'order_form_class.html', context)
    elif request.method == 'POST':
        form = OrderForm(request.POST)
        if not form.is_valid():
            context = {
                "title": "Редактирование заявки",
                'button_text': "Сохранить",
                "form": form,
            }
            return render(request, 'order_form_class.html', context)

        order = Order.objects.get(id=order_id)
        order.client_name = form.cleaned_data['client_name']
        order.phone = form.cleaned_data['phone']
        order.comment = form.cleaned_data['comment']
        order.master = form.cleaned_data.get('master')
        order.services.set(form.cleaned_data['services'])
        order.save()

        return redirect('thanks')

def reviews_create(request):
    if request.method == 'GET':
        form = ReviewModelForm()
        context = {
            "title": "Отзыв",
            'button_text': "Отправить отзыв",
            "form": form,
        }
        return render(request, 'review_form.html', context)
    elif request.method == 'POST':
        form = ReviewModelForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "title": "Отзыв",
                'button_text': "Отправить отзыв",
                "form": form,
            }
            return render(request, 'review_form.html', context, {'form': form})
        form.save()
        return redirect('thanks')
