import os
from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug, 1])
    

def get_upload_path(instance, filename):
    #  задаем название файла названием slug`а продукта
    filename = instance.slug + '.' + filename.split('.')[1]  
    return os.path.join('images/', filename)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    week = models.IntegerField(default=1)
    clpc = models.TextField(blank=True)
    image = models.ImageField(upload_to=get_upload_path, blank=True)
    star_rating = models.DecimalField(default=5.0, max_digits=5, decimal_places=2)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(default='default@mail.ru', max_length=100)
    written_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    star_rating = models.IntegerField(default=5)
    taste_rating = models.IntegerField(default=5)
    representability_rating = models.IntegerField(default=5)
    price_rating = models.IntegerField(default=5)
    description = models.TextField(blank=True)
    class Meta:
        ordering = ('written_at',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
    
    def __str__(self):
        return self.product
    

class StarRating(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    star_1 = models.IntegerField(default=0)
    star_2 = models.IntegerField(default=0)
    star_3 = models.IntegerField(default=0)
    star_4 = models.IntegerField(default=0)
    star_5 = models.IntegerField(default=0)
    class Meta:
        ordering = ('product_id',)
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        
    def __str__(self):
        return self.product


class Cafeteria(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    address = models.CharField(max_length=100, db_index=True)
    available = models.BooleanField(default=True)
    rows = models.IntegerField(default=6)
    cols = models.IntegerField(default=8)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('id',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Столовая'
        verbose_name_plural = 'Столовые'
    
    def __str__(self):
        return self.name
    

class Table(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField()
    cafeteria = models.ForeignKey(Cafeteria, on_delete=models.CASCADE)
    hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    row = models.IntegerField()
    col = models.IntegerField()
    order_id = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ('cafeteria_id', 'row', 'col')
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'


class TableTime(models.Model):
    id = models.AutoField(primary_key=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    ordered_at = models.CharField(max_length=10)
    class Meta:
        ordering = ('table_id', 'ordered_at')
        verbose_name = 'Время стола'
        verbose_name_plural = 'Время столов'


class ProductStatistics(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    morning = models.IntegerField(default="0")
    afternoon = models.IntegerField(default="0")
    evening = models.IntegerField(default="0")
    total = models.IntegerField(default="0")
    class Meta:
        verbose_name = 'Статистика по продуктам'
        verbose_name_plural = 'Статистика по продуктам'


class LunchPosition(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    day = models.IntegerField()
    class Meta:
        verbose_name = 'Позиция ланча'
        verbose_name_plural = 'Позиции ланча'


class UserLunch(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class UserLunchItems(models.Model):
    id = models.AutoField(primary_key=True)
    lunch = models.ForeignKey(UserLunch, on_delete=models.CASCADE)
    

@receiver(post_save, sender=Cafeteria)
def create_related_tables(sender, instance, created, **kwargs):
    if created:
        for row in range(1, instance.rows + 1):
            for col in range(1, instance.cols + 1):
              Table.objects.create(cafeteria=instance, number=instance.cols * (row - 1) + col, row=row, col=col)


@receiver(pre_delete, sender=Cafeteria)
def delete_related_tables(sender, instance, **kwargs):
    Table.objects.filter(cafeteria=instance).delete()
  


@receiver(pre_save, sender=Cafeteria)
def update_tables(sender, instance, **kwargs):
    if instance._state.adding:  # Check if the Cafeteria instance is being added for the first time
        return  # If so, do nothing

    old_cafeteria = Cafeteria.objects.get(pk=instance.pk)  # Get the current state of the Cafeteria instance
    old_rows = old_cafeteria.rows
    new_rows = instance.rows
    old_cols = old_cafeteria.cols
    new_cols = instance.cols

    used = {}

    if new_rows < old_rows:
        Table.objects.filter(row__gt=new_rows).delete()  # Delete Table objects with row value more than new_rows
    
    elif new_rows > old_rows:
        for row in range(old_rows + 1, new_rows + 1):
            for col in range(1, new_cols + 1):
                Table.objects.create(cafeteria=instance, number=instance.cols * (row - 1) + col, row=row, col=col) 
                used[(row, col)] = 1
    
    if new_cols < old_cols:
        Table.objects.filter(col__gt=new_cols).delete()

    elif new_cols > old_cols:
        for col in range(old_cols + 1, new_cols + 1):
            for row in range(1, new_rows + 1):
                if not used.get((row, col), 0):
                    Table.objects.create(cafeteria=instance, number=instance.cols * (row - 1) + col, row=row, col=col) 