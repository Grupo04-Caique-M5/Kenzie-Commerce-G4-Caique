from rest_framework import serializers
from .models import Order, StatusChoices
from products.serializers import ProductSerializer
from products.models import Product
from carts.serializers import CartProductSerializer, CartSerializer
from users.serializers import UserSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        status = serializers.ChoiceField(
            choices=StatusChoices, default=StatusChoices.ORDER_RECEIVED
        )

        model = Order
        fields = ["total_price", "vendor_id", "user", "cart_products", "status"]
        read_only_fields = ["user", "total_price"]


class OrderListSerializer(serializers.ModelSerializer):
    cart_products = ProductSerializer(read_only=True, many=True)
    orders = OrderSerializer(read_only=True, many=True, source="user.user_orders")

    def create(self, validated_data):
        user = validated_data.pop("user")
        cart = user.cart

        cart_products = user.cart.cart_cart.filter(cart=cart).values_list(
            "product", flat=True
        )
        new_products = [Product.objects.get(id=product) for product in cart_products]
        new_products_dict = ProductSerializer(new_products, many=True)  # ❗❗❗ OBS ❗❗❗

        # validated_data["cart_products"] = new_products_dict.data

        # prices_list = user.cart.cart_cart.filter(cart=cart).values_list(
        #     "product__price", flat=True
        # )
        # prices_list = [price for price in prices_list]
        # print("types_1", [type(price) for price in prices_list])
        # prices = list(prices_list)

        # validated_data["total_price"] = sum(prices_list)

        # vendors_list = user.cart.cart_cart.filter(cart=cart).values_list(
        #     "product__user", flat=True
        # )
        vendors = set([product["user"] for product in new_products_dict.data])

        list_orders = []

        for vendor in vendors:
            products = []
            user_cart = validated_data.copy()

            for product in new_products_dict.data:
                if vendor == product["user"]:
                    product.pop('storage')
                    products.append(product)

            prices_list = [float(product["price"]) for product in products]
            price = sum(prices_list)

            user_cart["total_price"] = price
            user_cart["vendor_id"] = vendor
            user_cart["cart_products"] = products
            order = Order.objects.create(**user_cart, user=user)
            list_orders.append(order)

        return list_orders

    def to_representation(self, instance):
        data = super().to_representation(instance)
        print(data)
        data["orders"] = OrderSerializer(instance, many=True).data

        return data

    class Meta:
        model = Order
        fields = ["total_price", "vendor_id", "cart_products", "orders", "status"]
        read_only_fields = ["user", "total_price"]
        extra_kwargs = {"orders": [{"cart_products": [{"user": {"write_only": True}}]}]}
