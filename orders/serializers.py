from rest_framework import serializers
from .models import Order, StatusChoices
from products.serializers import ProductSerializer
from products.models import Product
from carts.models import Cart
from .send_info import send_email


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=StatusChoices, default=StatusChoices.ORDER_RECEIVED
    )

    def update(self, instance, validated_data):
        if validated_data.get("status"):
            instance.status = validated_data.get("status")
            send_email(validated_data.get("status"), instance)
            instance.save()
            return instance

    class Meta:
        model = Order
        fields = [
            "id",
            "vendor_id",
            "total_price",
            "status",
            "user",
            "order_time",
            "cart_products",
        ]
        read_only_fields = ["user", "total_price"]


class OrderListSerializer(serializers.ModelSerializer):
    cart_products = ProductSerializer(read_only=True, many=True)
    orders = OrderSerializer(read_only=True, many=True, source="user.user_orders")

    def create(self, validated_data):
        user = validated_data.pop("user")
        cart = user.cart

        cart_products = cart.cart_cart.filter(cart=cart).values_list(
            "product", flat=True
        )

        new_products = [Product.objects.get(id=product) for product in cart_products]

        new_products_dict = ProductSerializer(new_products, many=True)
        vendors = set([product["user"] for product in new_products_dict.data])
        list_orders = []

        for vendor in vendors:
            products = []

            for product in new_products_dict.data:
                if vendor == product["user"]:
                    product.pop("storage")
                    products.append(product)

            prices_list = [float(product["price"]) for product in products]
            price = sum(prices_list)

            user_cart = validated_data.copy()
            user_cart["total_price"] = price
            user_cart["vendor_id"] = vendor
            user_cart["cart_products"] = products

            order = Order.objects.create(**user_cart, user=user)
            list_orders.append(order)

        cart.delete()

        Cart.objects.create(user=user)

        return list_orders

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["orders"] = OrderSerializer(instance, many=True).data

        return data

    class Meta:
        model = Order
        fields = [
            "id",
            "vendor_id",
            "status",
            "total_price",
            "orders",
            "cart_products",
        ]
        read_only_fields = ["user", "total_price"]
        extra_kwargs = {"orders": [{"cart_products": [{"user": {"write_only": True}}]}]}
