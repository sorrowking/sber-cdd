# Generated by Django 4.2.7 on 2023-11-17 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_table_order'),
        ('orders', '0005_rename_paid_order_ready_remove_order_owner_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='table',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='table', to='shop.table'),
        ),
        migrations.AddField(
            model_name='order',
            name='to_go',
            field=models.BooleanField(default=False),
        ),
    ]
