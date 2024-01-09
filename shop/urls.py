from django.contrib import admin
from django.urls import path

from shop.views import (
    product_list, 
    product_detail,
    about_us,
    lunch,
    lunch_products, 
    logout_view,
    comment_add,
    get_table,
    tables_by_time,
)

app_name = 'shop'

urlpatterns = [
    path('', product_list, name='product_list'),
    path('logout/', logout_view, name='logout_view'),
    path('lunch/<int:day>/', lunch, name="lunch"),
    path('lunch_products/', lunch_products, name="lunch_products"),
    path('about_us/', about_us, name='about_us'),
    path('get_table/', get_table, name='get_table'),
    path('tables_by_time/', tables_by_time, name=''),
    path('<str:category_slug>/<int:week>', product_list, name='product_list_by_category'),
    path('<int:id>/<str:slug>/', product_detail, name='product_detail'),
    path('comment/<int:product_id>/<str:username>/', comment_add, name='comment_view'),
]
