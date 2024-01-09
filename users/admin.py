from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display =['user', 'name', 'surname', 'lastname', 'sex', 'birthdate', 'email', 'phone', 'rating', 'image', 'created_at', 'updated_at', 'balance']
    list_filter = ['rating', 'created_at', 'updated_at']
    list_editable = ['rating', 'balance']

admin.site.register(Profile, ProfileAdmin)
