# Generated by Django 4.2.7 on 2024-02-28 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_order_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='email',
        ),
        migrations.RemoveField(
            model_name='order',
            name='phone',
        ),
    ]
