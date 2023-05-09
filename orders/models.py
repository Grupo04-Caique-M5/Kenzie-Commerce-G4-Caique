from django.db import models


class StatusChoices(models.TextChoices):
    ORDER_RECEIVED = "Pedido Realizado"
    ON_GOING = "Em Andamento"
    COMPLETE = "Entregue"


class Order(models.Model):
    status = models.CharField(
        max_length=30,
        choices=StatusChoices.choices,
        default=StatusChoices.ORDER_RECEIVED,
    )
    order_time = models.TimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    vendor_id = models.IntegerField(default=0)
    cart_products = models.JSONField(default={})
    user = models.ForeignKey(
        "users.User", on_delete=models.PROTECT, related_name="user_orders"
    )
