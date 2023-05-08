from rest_framework import serializers
from .models import Order
from products.serializers import ProductSerializer
from products.models import Product
from carts.serializers import CartProductSerializer
from users.serializers import UserSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["total_price", "vendor_id", "user", "cart_products"]
        read_only_fields = ["user", "total_price"]


class OrderListSerializer(serializers.ModelSerializer):
    cart_products = ProductSerializer(
        read_only=True, many=True
    )
    orders = OrderSerializer(
        read_only=True, many=True, source="user.user_orders"
    )

    def create(self, validated_data):
        user = validated_data.pop("user")
        cart = user.cart

        cart_products = user.cart.cart_cart.filter(cart=cart).values_list(
            "product", flat=True
        )
        new_products = [Product.objects.get(id=product) for product in cart_products]
        new_products_dict = ProductSerializer(new_products, many=True) # ❗❗❗ OBS ❗❗❗

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

        list_orders = []

        for vendor in vendors:
            products = []
            user_cart = validated_data.copy()

            for product in validated_data["cart_products"]:
                if vendor == product["user"]:
                    products.append(product)

            user_cart["vendor_id"] = vendor
            user_cart["cart_products"] = products
            order = Order.objects.create(**validated_data, user=user)
            list_orders.append(order)

        
        return list_orders

    def to_representation(self, instance):
        """
        Override the to_representation method to include the serialized
        data for the related objects in the response.
        """
        print(instance)
        data = super().to_representation(instance)
        # Include the serialized data for the related objects.
        data["orders"] = OrderSerializer(instance, many=True).data
        return data

    class Meta:
        model = Order
        fields = ["total_price", "vendor_id", "cart_products", "orders"]
        read_only_fields = ["user", "total_price"]
