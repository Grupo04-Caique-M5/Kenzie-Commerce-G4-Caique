from rest_framework import serializers
from .models import Order
from users.serializers import UserSerializer
from carts.models import Cart
from products.models import Product
from products.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)

    def create(self, validated_data):
        orders = []
        user = validated_data.pop("user")
        user_cart = Cart.objects.get(user_id=user.id)
        cart_products = Product.objects.filter(carts=user_cart)
        all_products = ProductSerializer(cart_products, many=True)
        print(all_products.data)

        return Order.objects.create(**validated_data, user=user, cart=user_cart)

    class Meta:
        model = Order
        fields = ["status", "order_time", "total_price", "vendor_id", "user", "cart"]
        read_only_fields = ["cart", "user"]
