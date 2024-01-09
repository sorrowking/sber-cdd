from django.contrib import admin

from .models import Order, OrderItem
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'ready', 'updated', 'in_cafe', 'profile_id', 'table', 'reserve_time']
    list_filter = ['ready', 'created', 'updated']
    list_editable = ['ready', 'table', 'in_cafe', 'reserve_time']
    inlines = [OrderItemInline]
admin.site.register(Order, OrderAdmin)
