from django.urls import path
from .views import (edit_product, add_product, login, set_tables, ProductDeleteView, order_is_applied,
                     product, pending_orders, ready_orders, table_list, logout_view, order_is_ready, statistics)
from django.views.generic import RedirectView
from .views import ProductDeleteView
from .views import ProductDetailView

app_name = 'staff'

urlpatterns = [
    path('pending_orders/', pending_orders, name='pending_orders'),
    path('ready_orders/', ready_orders, name='ready_orders'),

    path('order_is_ready/<int:id>', order_is_ready, name='order_is_ready'),
    path('order_is_applied/<int:id>', order_is_applied, name='order_is_applied'),

    path('product/', product, name='product'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:id>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('edit_product/<int:product_id>/', edit_product, name='edit_product'),
    path('add_product/', add_product, name='add_product'),

    path('set_tables/', set_tables, name='set_tables'),
    path('table_list/', table_list, name='table_list'),

    path('statistics/<int:category>/<int:day_time>', statistics, name='statistics'),

    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout_view')
]