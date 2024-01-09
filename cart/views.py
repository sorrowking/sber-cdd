from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse
from datetime import datetime, timedelta
from shop.models import Product, Cafeteria, Table, TableTime
from users.models import Profile
from orders.models import Order, OrderItem
from .cart import Cart
from .forms import CartAddProductForm
from django.template.defaultfilters import slugify
from config.views import get_natural_range
from django import template

@require_POST
def in_cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:cart_detail')

@require_POST
def cart_add(request, product_id, category_slug=None):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect(reverse('shop:product_list_by_category', kwargs={'category_slug': category_slug, 'week': 1}))


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, 'Удалено')
    return redirect('cart:cart_detail')


    
def cart_detail(request):
    cart = Cart(request)
    cafeteria = Cafeteria.objects.get(id=3)
    tables = Table.objects.filter(cafeteria_id=3)  # ОТОБРАЖЕНИЕ ТЕКУЩЕЙ КАФЕТЕРИИ TODO
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    context = {'cart': cart, 'cafeteria': cafeteria, 'tables': tables,
                'time_periods': get_time_segments(),}
    return render(request, 'cart/detail.html', context)


def business_detail(request):
    ids = [13, 15, 17, 29]
    cart = Product.objects.filter(id__in=ids) # ОТОБРАЖЕНИЕ ТЕКУЩЕЙ КАФЕТЕРИИ TODO
    cafeteria = Cafeteria.objects.get(id=3)
    tables = Table.objects.filter(cafeteria_id=3)  # ОТОБРАЖЕНИЕ ТЕКУЩЕЙ КАФЕТЕРИИ TODO
    context = {'cart': cart, 'cafeteria': cafeteria, 'tables': tables,
                'time_periods': get_time_segments(), 'business': True}
    return render(request, 'cart/business_detail.html', context)


def get_time_segments():
    current_time = datetime.now()
    hours = current_time.hour
    minutes = current_time.minute
    time_segments = []

    while hours != 0 or minutes != 0:
        time_segments.append(f"{hours:02d}:{minutes:02d}")
        if minutes < 30:
            minutes = 30
        else:
            minutes = 0
            hours = (hours + 1) % 24
    return time_segments[2:]


def user_order(request, order_id=0):
    orders_before = 0
    profile = Profile.objects.get(email=request.user.email)
    all_orders = Order.objects.filter(profile_id=profile.id)
    current_table = None
    if not order_id:
        order = Order.objects.filter(profile_id=profile.id).first()
    else:
        order = Order.objects.get(id=order_id)
    if order is None:
        order_items = None
        return render(request, 'cart/user_order.html', {'order': order})
    else:
        if order.in_cafe:
            current_table = order.table
        orders_before = Order.objects.filter(reserve_time=order.reserve_time, id__lt=order.id).count() + 1
        order_items = OrderItem.objects.filter(order_id=order.id)
    cafeteria = Cafeteria.objects.get(id=3)
    tables = Table.objects.filter(cafeteria_id=3)  # ОТОБРАЖЕНИЕ ТЕКУЩЕЙ КАФЕТЕРИИ TODO
    context = {'order_items': order_items, 'order': order, 'all_orders': all_orders, 'orders_before': orders_before,
               'cafeteria': cafeteria, 'tables': tables, 'current_table': current_table, 'profile': profile}
    return render(request, 'cart/user_order.html', context)

