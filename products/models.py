from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    storage = models.IntegerField()
    available = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(
        "categories.Category", on_delete=models.PROTECT, related_name="product"
    )
    user = models.ForeignKey(
        "users.User", on_delete=models.PROTECT, related_name="users"
    )
