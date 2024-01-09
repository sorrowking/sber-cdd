from django.db import models
from shop.models import Product, Table
from users.models import Profile
from django.urls import reverse

class Order (models.Model):
    id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(Profile, related_name='order', null=True, blank=True, on_delete=models.CASCADE)
    ready = models.BooleanField(default=False)  # готов ли заказ
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    in_cafe = models.BooleanField(default=False)
    reserve_time = models.CharField(max_length=10, default="13:30")
    table = models.ForeignKey(Table, related_name='table', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return 'Заказ {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_absolute_url(self):
        return reverse('cart:user_order_special', args=[self.id])


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


