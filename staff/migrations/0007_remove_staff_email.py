# Generated by Django 4.2.7 on 2023-11-22 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0006_delete_type_staff_user_alter_staff_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='email',
        ),
    ]
