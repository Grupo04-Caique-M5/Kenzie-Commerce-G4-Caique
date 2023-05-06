# Generated by Django 4.2 on 2023-05-06 16:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("carts", "0010_alter_cart_products"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="products",
        ),
        migrations.AlterField(
            model_name="cart",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="cart",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
