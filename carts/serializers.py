from rest_framework import serializers
from rest_framework.response import Response
from .models import Cart, CartProducts
from products.serializers import ProductSerializer
from products.models import Product
from django.shortcuts import get_object_or_404


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartProducts
        fields = ["product", "cart"]
        read_only_fields = []
        extra_kwargs = {"cart": {"write_only": True}}


class CartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    cart_products = CartProductSerializer(many=True, read_only=True, source="cart_cart")

    def create(self, validated_data: dict):
        user = validated_data.pop("user")

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user)

        product = get_object_or_404(
            Product,
            id=validated_data["product_id"],
        )

        if product.storage == 0:
            raise KeyError("product is empty in storage")

        CartProducts.objects.create(product=product, cart=cart)

        return cart

    class Meta:
        model = Cart
        fields = ["product_id", "user", "cart_products"]
        read_only_fields = ["user", "products"]

