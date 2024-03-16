# Generated by Django 4.2.7 on 2024-03-15 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_product_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, to='product.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(blank=True, null=True, related_name='products', to='product.size'),
        ),
    ]
