from rest_framework import serializers
from .models import Order
from products.serializers import ProductSerializer
from products.models import Product
from carts.serializers import CartProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    cart_products = CartProductSerializer(
        read_only=True, many=True, source="user.cart.cart_cart"
    )

    def create(self, validated_data):
        user = validated_data.pop("user")
        cart = user.cart

        cart_products = user.cart.cart_cart.filter(cart=cart).values_list(
            "product", flat=True
        )
        new_products = [Product.objects.get(id=product) for product in cart_products]
        new_products_dict = ProductSerializer(new_products, many=True)

        validated_data["cart_products"] = new_products_dict.data

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
            return Order.objects.create(**validated_data, user=user)
        
        #falta criar para vendores diferentes

    class Meta:
        model = Order
        fields = ["total_price", "vendor_id", "user", "cart_products"]
        read_only_fields = ["user", "total_price"]
