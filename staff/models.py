from django.db import models

from django.contrib.auth.hashers import make_password
from shop.models import Product
from shop.models import Category
from django.contrib.auth.models import User
import uuid, os
    

class Staff(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, unique=True)
    password = models.TextField()
    staff_id = models.IntegerField()
    logged = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if len(self.password) < 60:
            self.password = make_password(self.password)
        
        super().save(*args, **kwargs)


class StaffProduct(models.Model):
    id = models.AutoField(primary_key=True)
    available = models.BooleanField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    slug = models.SlugField(max_length=100, db_index=True)
    name = models.CharField(max_length=100, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    original_product = models.OneToOneField(Product, on_delete=models.CASCADE)

    # Добавь другие необходимые поля для модели StaffProduct

    def __str__(self):
        return self.name
    
    