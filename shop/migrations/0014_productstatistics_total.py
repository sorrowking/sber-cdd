# Generated by Django 4.2.7 on 2023-11-24 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_productstatistics'),
    ]

    operations = [
        migrations.AddField(
            model_name='productstatistics',
            name='total',
            field=models.IntegerField(default='0'),
        ),
    ]