from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
from config.views import get_natural_range
from .models import OrderItem, Order
from cart.cart import Cart
from users.models import Profile 
from shop.models import Table, TableTime, ProductStatistics

import qrcode, random, string


def pin_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def pin_create(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        if len(phone) == 16:
            phone = phone.replace('+', '').replace('(', '').replace(')', '').replace('-', '').replace('7', '', 1)
        try:
            profile = Profile.objects.get(phone=phone)
            if profile.user.username != '':
                profile.pincode = pin_generator()
                profile.save()
                response = {
                    'username': profile.name,
                    'pincode': profile.pincode
                }
        except:
            response = {'error': 'Пользователь не найден'}
    return JsonResponse(response)


def order_create(request):
    cart = Cart(request)
    profile = Profile.objects.get(email=request.user.email)
    if request.method == 'POST':
        order = Order.objects.create()
        time = 0
        if not int(request.POST['chosenTableId']):
            order.in_cafe = False
        else:
            order.in_cafe = True
            table = Table.objects.get(id=request.POST['chosenTableId'])
            order.table = table
            time = request.POST['chosenTableTime']
            order.reserve_time = time
            table.order_id = order.id
            table_time = TableTime.objects.create(table_id=table.id, ordered_at=time)
            table.save()
        order.profile = profile
        order.save()
        profile.rating += 1
        data = {'order': 0, 'profile': 0}
        for item in cart:
            if time:
              print(int(item['quantity']))
              try:
                  product_stat = ProductStatistics.objects.get(product=item['product'])
              except:
                  product_stat  = ProductStatistics.objects.create(product=item['product'])
              if time < "11:59":
                  product_stat.morning = int(product_stat.morning) + int(item['quantity'])
              elif time < "17:59":
                  product_stat.afternoon = int(product_stat.afternoon) + int(item['quantity'])
              else:
                  product_stat.evening = int(product_stat.evening) + int(item['quantity'])
              product_stat.total = int(product_stat.total) + int(item['quantity'])
              product_stat.save() 

            OrderItem.objects.create(
                order = order,
                product = item['product'],
                price = item['price'],
                quantity = item['quantity']
            )
        profile.balance -= order.get_total_cost()
        profile.save()
        data['order'] = order
        data['profile'] = profile
        img = qrcode.make(data)
        img.save("media/qr/" + str(order.id) + ".png")
        cart.clear()
        send_mail(
            'Заказ Оформлен', 
            'Войдите в админ панель, что бы просмотреть новый заказ.' , 
            'info@it-cube.krk', 
            ['manager@it-cube.krk'], 
            fail_silently=False
        )
    return redirect('shop:product_list')

