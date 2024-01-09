from django.db import models
from django.contrib.auth.models import User
import uuid, os

def get_upload_path(instance, filename):
    filename = instance.user.username + '.' + filename.split('.')[1]  
    return os.path.join('profile_images/', filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField('Имя', max_length=50, default="Иван")
    surname = models.CharField('Фамилия', max_length=50, default="Иванович")
    lastname = models.CharField('Отчество', max_length=50, default="Иванович")
    SEX_CHOICE = (
        ('М', 'Мужской'),
        ('Ж', 'Женский')
    )
    sex = models.CharField('Пол', max_length=1, choices=SEX_CHOICE, default="М")
    birthdate = models.DateField('Дата рождения', default="2000-01-01")
    email = models.CharField('Адрес электронной почты', max_length=100, default="default@mail.ru")
    phone = models.CharField(max_length=10, blank=True, null=True)
    rating = models.PositiveIntegerField(default=0)
    pincode = models.CharField(max_length=6, blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to=get_upload_path, default="profile_images/default.jpg")
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
 
    def __str__(self):
        return self.email
 
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
