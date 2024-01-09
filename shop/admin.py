from django.contrib import admin

from .models import (Category, Product, Comment, StarRating, UserLunch, UserLunchItems,
                      Cafeteria, Table, TableTime, ProductStatistics, LunchPosition)
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created_at', 'updated_at']
    list_filter = ['available', 'created_at', 'updated_at']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'user', 'written_at', 'star_rating', 'taste_rating', 
                    'representability_rating', 'price_rating', 'description']
    list_editable = ['description']

admin.site.register(Comment, CommentAdmin)


class StarRatingAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'star_1', 'star_2', 'star_3', 'star_4', 'star_5']
    list_editable = ['star_1', 'star_2', 'star_3', 'star_4', 'star_5']

admin.site.register(StarRating, StarRatingAdmin)


class CafeteriaAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name', 'address', 'available', 'rows', 'cols', 'created_at', 'description']
    list_editable = ['address', 'available', 'rows', 'cols', 'description']


admin.site.register(Cafeteria, CafeteriaAdmin)


class TableAdmin(admin.ModelAdmin):
    list_display = ['id', 'hidden', 'number', 'row', 'col', 'created_at', 'order_id']
    list_editable = ['hidden','order_id', 'number']


admin.site.register(Table, TableAdmin)


class TableTimeAdmin(admin.ModelAdmin):
    list_display = ['id', 'table', 'ordered_at', ]
    list_editable = ['table', 'ordered_at', ]


admin.site.register(TableTime, TableTimeAdmin)


class LunchPositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'day', 'category', 'product']
    list_editable = ['day', 'category', 'product']


admin.site.register(LunchPosition, LunchPositionAdmin)


class ProductStatisticsAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'morning', 'afternoon', 'evening', 'total']


admin.site.register(ProductStatistics, ProductStatisticsAdmin)


class UserLunchAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']


admin.site.register(UserLunch, UserLunchAdmin)


class UserLunchItemsAdmin(admin.ModelAdmin):
    list_display = ['id', 'lunch']


admin.site.register(UserLunchItems, UserLunchItemsAdmin)
