# Generated by Django 4.2.7 on 2023-11-10 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_product_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='clpc',
            field=models.TextField(blank=True),
        ),
    ]