# Generated by Django 4.2 on 2023-05-05 21:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_initial"),
        ("carts", "0004_remove_cart_products_cartproducts"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="products",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="carts",
                to="products.product",
            ),
            preserve_default=False,
        ),
    ]
