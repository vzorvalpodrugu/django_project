from django.shortcuts import render

from core.data import masters, services, orders


def landing(request):
    context = {
        "masters": masters,
        "title": "Barbershop Landing Page",
        "services": services
    }
    return render(request, 'landing.html', context)

def thanks(request):
    context = {
        "text" : "Заявка принята!"
    }
    return render(request, 'thanks.html', context)

def orders_list(request):
    context = {
        "orders": orders,
        "title": "Список заявок"
    }
    return render(request, 'orders_list.html', context)

def orders_detail(request, order_id):
    try:
        order = [order for order in orders if order['id'] == order_id][0]
    except IndexError:
        return render(request, '404.html', status=404)

    context = {
        "order": order
    }
    return render(request, 'orders_detail.html', context)