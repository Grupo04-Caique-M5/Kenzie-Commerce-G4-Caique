from django.db import models


class Cart(models.Model):
    products = models.ManyToManyField("products.Product", related_name="carts")
    user = models.ForeignKey(
        "users.User", on_delete=models.PROTECT, related_name="user_carts"
    )
