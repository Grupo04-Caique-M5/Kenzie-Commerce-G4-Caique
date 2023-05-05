from rest_framework import serializers
from rest_framework.response import Response
from .models import Cart
from products.serializers import ProductSerializer
from products.models import Product
from django.shortcuts import get_object_or_404


class CartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    products = ProductSerializer(
        many=True,
        read_only=True
    )

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

        product.carts.add(cart)
        product.save()
        all_products = Product.objects.filter(carts=cart)
        self.products = all_products
        return cart


    class Meta:
        model = Cart
        fields = [
            "product_id",
            "products",
            "user",
        ]
        read_only_fields = [
            "user"
        ]


# class CartProductSerializer(serializers.ModelSerializer):
#     buyed_by = serializers.SerializerMethodField()

#     def get_buyed_by(self, obj):
#         return obj.id

#     def create(self, validated_data: dict) -> CartProducts:
#         user_id = self.get_buyed_by(self.instance)
#         validated_data["buyed_by"] = user_id

#         product = self.context.get("product")

#         if product:
#             validated_data["product"] = product

#         return CartProducts.objects.create(**validated_data)


#     class Meta:
#         model = CartProducts
#         fields = ["product"]
