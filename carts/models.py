from django.db import models


class Cart(models.Model):
    user = models.OneToOneField(
        "users.User",
        on_delete=models.PROTECT,
        related_name="cart",
    )
    # products = models.ForeignKey(
    #     "products.Product",
    #     related_name="carts",
    #     on_delete=models.PROTECT,
    #     null=True,
    #     default=None
    # )


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
    storage = models.IntegerField(default=1)
