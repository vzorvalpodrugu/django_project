from django.shortcuts import render
from core.data import masters, services, orders
# from django.contrib.auth.models import User
#
# user = User.objects.get(username='your_username')
# user.is_staff = True
# user.save()


def landing(request):
    context = {
        "masters": masters,
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
    # Временный хак для теста: если пользователь не авторизован, считаем его is_staff
    if not request.user.is_authenticated:
        class DummyUser:
            is_staff = True
        request.user = DummyUser()
    if not request.user.is_staff:
        return render(request, '403.html', status=403)
    context = {
        "orders": orders,
        "title": "Список заявок"
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
