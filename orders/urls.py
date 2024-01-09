from django.urls import path
from .views import order_create, pin_create
 
app_name = 'orders'
 
urlpatterns = [
    path('create/', order_create, name='order_create'),
    path('create/pin_create/', pin_create, name='pin_create'),
]