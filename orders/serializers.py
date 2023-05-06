from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = validated_data.pop("user")
        cart = user.cart

        prices_list = user.cart.cart_cart.filter(cart=cart).values_list(
            "product__price", flat=True
        )

        prices_list = [price for price in prices_list]

        prices = list(prices_list)

        validated_data["total_price"] = sum(prices)

        vendors_list = user.cart.cart_cart.filter(cart=cart).values_list(
            "product__user", flat=True
        )

        vendors = list(set(vendors_list))

        for vendor in vendors:
            validated_data["vendor_id"] = vendor
            print(validated_data)
            # order = Order.objects.create(**validated_data, user=user, cart=cart)

    class Meta:
        model = Order
        fields = ["total_price", "vendor_id", "user", "cart"]
        read_only_fields = ["user", "cart"]
