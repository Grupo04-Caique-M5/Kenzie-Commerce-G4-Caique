# Generated by Django 4.2 on 2023-05-06 20:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0004_alter_order_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="cart",
        ),
        migrations.AddField(
            model_name="order",
            name="cart_products",
            field=models.JSONField(default=[]),
        ),
    ]
