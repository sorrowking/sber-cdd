import datetime
import json
from django.forms.models import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from .models import Category, Product, StarRating, Comment, LunchPosition
from cart.cart import Cart
from staff.models import Staff
from .forms import CommentForm, StarRatingForm, ProductStarRatingUpdateForm
from cart.forms import CartAddProductForm
from users.views import user_registration
from users.forms import LoginForm, RegistrationForm
from decimal import Decimal, ROUND_HALF_UP
from django import template
from config.views import get_natural_range
from django.http import JsonResponse
from .models import Cafeteria, Table, TableTime
from django.views.decorators.http import require_GET


def product_list(request, category_slug=None, week=1):
    staff_id = 3
    try:
        staff_id = Staff.objects.get(user_id=request.user.id).staff_id
    except:
        pass
    login_error = ""
    registration_error = ""
    if request.method == "POST":
        errors = user_registration(request)
        login_error, registration_error = errors["login_error"], errors["registration_error"]
    registration_form = RegistrationForm()
    login_form = LoginForm()
    category = None
    week_url = '/all/'
    comments = Comment.objects.exclude(description="")
    categories = Category.objects.all().order_by('-created_at')
    products = Product.objects.filter(available=True) & Product.objects.filter(week=week)
    if category_slug and category_slug != 'all':
        week_url = '/' + category_slug + '/'
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category) & Product.objects.filter(week=week)

    today = datetime.date.today()
    dayOfWeek = today.weekday()

    lastTuesday = (today - datetime.timedelta(days=dayOfWeek-1)).strftime('%Y-%m-%d').replace('-', '.')
    nextTuesday = (today + datetime.timedelta(days=7-dayOfWeek)).strftime('%Y-%m-%d').replace('-', '.')
    nextnextTuesday = (today + datetime.timedelta(days=14-dayOfWeek)).strftime('%Y-%m-%d').replace('-', '.')
    if category_slug is None:
        category_slug = 'all'
    context = {
        'form_dict': {
            'login_form': login_form,
            'registration_form': registration_form,
        },
        'category': category,
        'category_slug': category_slug,
        'categories': categories,
        'products': products,
        'login_error': login_error,
        'registration_error': registration_error,
        'week_url': week_url,
        'comments': comments,
        'week': week,
        'tuesdays': {'last': lastTuesday, 'next': nextTuesday, 'nextnext': nextnextTuesday,} ,
        'staff_id': staff_id,
    }

    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'cart_product_form': cart_product_form
    }
    return render(request, 'shop/product/detail.html', context)


def get_lunch_dates():
    dates = []
    today = datetime.datetime.today().date()
    for i in range(14):
        dates.append(today + datetime.timedelta(days=i))
    return dates


def lunch(request, day=1):
    deserts = LunchPosition.objects.filter(category_id=9).filter(day=day)
    salads = LunchPosition.objects.filter(category_id=8).filter(day=day)
    garnishes = LunchPosition.objects.filter(category_id=7).filter(day=day)
    soups = LunchPosition.objects.filter(category_id=6).filter(day=day)
    drinks = LunchPosition.objects.filter(category_id=5).filter(day=day)
    dates = get_lunch_dates()
    context = {
        "categories": [["Салат", salads], ["Суп", soups], ["Гарнир", garnishes], ["Десерт", deserts], ["Напиток", drinks]],
        "dates":  [[ind + 1, el] for ind, el in enumerate(dates)],
        'day': day, "cur_date": datetime.datetime.today().date() + datetime.timedelta(days=day - 1),
    }

    return render(request, 'shop/product/lunch.html', context)


def lunch_products(request): # TODO
    cart = Cart(request)
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_positions = list(map(int, data['selectedPositions']))
        products = Product.objects.filter(id__in=selected_positions)
        for product in products:
            cart.add(product=product, quantity=1, update_quantity=False)
    return render(request, 'cart/detail.html', {})


def news(request):
    return render(request, 'shop/product/news.html')

@require_POST
def comment_add(request, product_id, username):
    data = request.POST
    product = get_object_or_404(Product, id=product_id)
    comment_data = {"user": username, "taste_rating": data['taste-rating'], "representability_rating": data['representability-rating'],
                    "price_rating": data['price-rating'], "description": data['comment-text'], "product": product_id}
    now_rating = StarRating.objects.filter(product_id=product_id)
    total_rating = 0
    average_rating = round((int(comment_data["price_rating"]) + int(comment_data["taste_rating"]) + int(comment_data["representability_rating"])) / 3)
    if now_rating.count():
        now_rating = StarRating.objects.get(product_id=product_id)
        rating_data = model_to_dict(now_rating, fields=[field.name for field in now_rating._meta.fields])
        user_comments = Comment.objects.filter(user=username, product_id=product_id)
        if user_comments.count():
            for com in user_comments:
                com_rating = com.star_rating
                rating_data[f'star_{str(com_rating)}'] -= 1
                com.delete()
        rating_data[f'star_{str(average_rating)}'] += 1
        rating_sum = 0
        rating_count = 0
        for key in rating_data.keys():
            if "star" in key:
                rating_sum += rating_data[key] * int(key.split("_")[1])
                rating_count += rating_data[key]
        total_rating = Decimal(rating_sum / rating_count).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        rating_form = StarRatingForm(rating_data, instance=now_rating)
        rating_form.save()
    else:
        rating_data = {"star_1": 0, "star_2": 0, "star_3": 0, "star_4": 0, "star_5": 0, "product": product_id}
        rating_data[f'star_{str(average_rating)}'] += 1
        total_rating = Decimal(average_rating).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        rating_form = StarRatingForm(rating_data)
        rating_form.save()
    comment_data["star_rating"] = average_rating
    comment_form = CommentForm(comment_data)
    comment_form.save()
    product_upd = ProductStarRatingUpdateForm({"star_rating": total_rating}, instance=product)
    product_upd.save()
    return redirect('shop:product_list')


@require_GET
def get_table(request):
    tableseatId = request.GET.get('seatId')
    try:
        table = Table.objects.get(id=tableseatId)
        data = {
            'number': table.number,
            'id': table.id,
        }
    except Table.DoesNotExist:
        data = {
            'number': "",
            'id': 0,
        }
    return JsonResponse(data)


@require_GET
def tables_by_time(request):
    selectedTime = request.GET.get('selectedTime')
    tables = Table.objects.filter(cafeteria_id=3)  # TODO
    table_times = TableTime.objects.filter(ordered_at=selectedTime)
    data = {'tables': []}
    for table in tables:
        if not table_times.filter(table_id=table.id):
            data['tables'].append('')
        else:
            data['tables'].append('occupied')
    return JsonResponse(data)


def logout_view(request):
    user_id = request.user.id
    try:
        staff = get_object_or_404(Staff, user_id=user_id)
        staff.logged = False
        staff.save()
    except:
        pass
    logout(request)
    return redirect('shop:product_list')

def about_us(request):
    return render(request, 'shop/product/about_us.html')
