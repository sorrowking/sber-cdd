from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password
from staff.models import Staff
from orders.models import Order
from shop.models import Product, Table, Cafeteria, ProductStatistics, Category
from .forms import ProductForm
from config.views import get_natural_range
import json


def check_login(request):
    user_id = request.user.id
    staff = get_object_or_404(Staff, user_id=user_id)
    if staff.logged:
        return True
    return False


def login(request):
    user_id = request.user.id
    staff = get_object_or_404(Staff, user_id=user_id)
    if staff.logged:
        return redirect(reverse('staff:pending_orders'))
    err = ""
    if request.method == 'POST':
        user_password = request.POST.get('password')
        if check_password(user_password, staff.password):
            staff.logged = True
            staff.save()
            return redirect(reverse('staff:pending_orders'))
        else:
            err = "Неверный пароль"
            return render(request, 'staff/login.html', {"error": err})
    return render(request, 'staff/login.html', {"error": err})


def pending_orders(request):
    if not check_login(request):
       return redirect(reverse("staff:login"))
    orders = Order.objects.filter(ready=False).order_by('reserve_time', 'id')
    return render(request, 'staff/pending_orders.html', {'orders': orders})

# связь с pending
def order_is_ready(request, id):
    order = Order.objects.get(id=id)
    order.ready = True
    order.save()
    return redirect(reverse("staff:pending_orders"))


def ready_orders(request):
    if not check_login(request):
       return redirect(reverse("staff:login"))
    orders = Order.objects.filter(ready=True).order_by('reserve_time', 'id')
    return render(request, 'staff/ready_orders.html', {'orders': orders})


# связь с ready
def order_is_applied(request, id):
    order = Order.objects.get(id=id)
    order.delete()
    return redirect(reverse("staff:ready_orders"))

    
def product(request):
    if not check_login(request):
        return redirect(reverse("staff:login"))
    products = Product.objects.all().order_by('id')
    return render(request, 'staff/manage_pl.html', {'products': products})


def add_product(request):
    if not check_login(request):
       return redirect(reverse("staff:login"))
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('staff:login'))
    else:
        form = ProductForm()
    return render(request, 'staff/add_product.html', {'form': form})


def edit_product(request, product_id):
    if not check_login(request):
       return redirect(reverse("staff:login"))
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect(reverse('staff:login'))
    else:
        form = ProductForm(instance=product)
    return render(request, 'staff/edit_product.html', {'form': form, 'product': product})


def table_list(request):
    if not check_login(request):
        return redirect(reverse("staff:login"))
    cafeteria = Cafeteria.objects.get(id=3)
    if request.method == "POST":
        cafe_rows, cafe_cols = request.POST.get("cafe_rows"), request.POST.get("cafe_cols")
        cafeteria.rows = int(cafe_rows)
        cafeteria.cols = int(cafe_cols)
        cafeteria.save()
    tables = Table.objects.filter(cafeteria_id=3)
    context = {
        "tables": tables,
        "cafeteria": cafeteria,
    }
    return render(request, 'staff/edit_tables.html', context)

def set_tables(request):
    if not check_login(request):
        return redirect(reverse("staff:login"))
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_seats = list(map(int, data['selectedSeats']))
        action = data.get('action')
        tables = Table.objects.filter(id__in=selected_seats)
        if action == "HIDE":
            for table in tables:
                table.hidden = True
                table.save()
        else:
            for table in tables:
                table.hidden = False
                table.save()
    return redirect(reverse('staff:table_list'))


def statistics(request, category=0, day_time=0):
    initial = ProductStatistics.objects.all()
    if category:
        initial = initial.filter(product__category_id=category)
    if day_time == 1:
        statistics = initial.order_by('-morning')
    elif day_time == 2:
        statistics = initial.order_by('-afternoon')
    elif day_time == 3:
        statistics = initial.order_by('-evening')
    else:
        statistics = initial.order_by('-total')
    day_times = [[i, el] for i, el in enumerate(['Общие', 'Утром', 'Днем', 'Вечером'])]
    categories = Category.objects.all()
    context = {'statistics': statistics, 'categories': categories, 'day_times': day_times,
               'cur_category': category, 'cur_day_time': day_time,}
    return render(request, 'staff/statistics.html', context)


def logout_view(request):
    user_id = request.user.id
    try:
        staff = get_object_or_404(Staff, user_id=user_id)
        staff.logged = False
        staff.save()
    except:
        pass
    return redirect('shop:product_list')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('login/')  
 

class ProductDetailView(View):
    def get(self, request, id, slug):
        product = get_object_or_404(Product, id=id, slug=slug)

    def get(self, request, id, slug):
        product = get_object_or_404(Product, id=id, slug=slug)
        return render(request, self.template_name, {'product': product})
