# Generated by Django 4.2 on 2023-05-06 13:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("carts", "0007_cart_products_alter_cart_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="products",
        ),
    ]
