from django.contrib import admin
from .models import Staff

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['user', 'password', 'staff_id']
    list_editable = ['password', 'staff_id']
