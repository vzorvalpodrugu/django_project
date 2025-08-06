from django.urls import reverse

def get_context_menu(request):
    context = {
        "menu" : [
            {
               "name": "Главная",
               "url": reverse("landing")
           },
           {
               "name": "О нас",
               "url": reverse("landing") + "#about"
           },
           {
               "name": "Услуги",
               "url": reverse("landing") + "#services"
           },
           {
               "name": "Мастера",
               "url": reverse("landing") + "#masters"
           },
           {
               "name": "Запись",
               "url": reverse("landing") + "#booking"
           },
           {
               "name": "Управление",
               "url": reverse("orders_list")
           }
       ]
    }
    return context