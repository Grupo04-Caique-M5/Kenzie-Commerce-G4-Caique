from django.db import models


class Cart(models.Model):
    user = models.OneToOneField(
        "users.User",
        on_delete=models.PROTECT,
        related_name="cart",
    )


class CartProducts(models.Model):
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="cart_product",
    )
    cart = models.ForeignKey(
        "carts.Cart",
        on_delete=models.CASCADE,
        related_name="cart_cart",
    )
