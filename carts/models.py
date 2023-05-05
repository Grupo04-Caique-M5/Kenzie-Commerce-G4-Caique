from django.db import models


class Cart(models.Model):
    products = models.ManyToManyField(
        "products.Product", 
        related_name="carts",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="user_carts",
    )


# class CartProducts(models.Model):
#     product = models.ForeignKey(
#         "carts.Cart",
#         on_delete=models.CASCADE,
#         related_name="cart_product",
#     )
#     buyed_by = models.ForeignKey(
#         "users.User",
#         on_delete=models.CASCADE,
#         related_name="user_buyed_by",
#     )
