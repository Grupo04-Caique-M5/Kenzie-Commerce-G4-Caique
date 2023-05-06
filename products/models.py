from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    storage = models.IntegerField()
    available = models.BooleanField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(
        "categories.Category", on_delete=models.PROTECT, related_name="product"
    )
    user = models.ForeignKey(
        "users.User", on_delete=models.PROTECT, related_name="users"
    )

    def save(self, *args, **kwargs):
        if self.storage == 0:
            self.available = False
        else:
            self.available = True
        super(Product, self).save(*args, **kwargs)
