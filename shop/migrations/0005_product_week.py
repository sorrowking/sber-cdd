# Generated by Django 4.2.7 on 2023-11-09 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_category_id_alter_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='week',
            field=models.IntegerField(default=1),
        ),
    ]