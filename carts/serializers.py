from rest_framework import serializers
from rest_framework.response import Response
from .models import Cart, CartProducts
from products.serializers import ProductSerializer
from products.models import Product
from django.shortcuts import get_object_or_404


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProducts
        fields = ["product", "cart"]
        # read_only_fields = []
        # extra_kwargs = {"user": {"write_only": True}}


class CartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    # cart_products = CartProductSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    # products = serializers.SerializerMethodField(method_name="get_products")

    # def get_products(self, obj):
    #     cart = Cart.objects.filter(user=self.context["request"].user).first()

    #     if cart:
    #         teste = CartProducts.objects.filter(cart=cart).values_list(
    #             "product", flat=True
    #         )
    #         print("teste", teste)
    #         return teste
    #     return []

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

        # verify_product = CartProducts.objects.filter(product=product).first()

        # print(verify_product)

        # if verify_product:
        #     verify_product.storage += 1
        #     verify_product.save()
        #     print(verify_product.storage)
        #     return verify_product

        cart_product = CartProducts.objects.create(product=product, cart=cart)

        # all_products = Product.objects.filter(cart_product=cart_product)
        teste = CartProducts.objects.filter(cart=cart).values_list("product", flat=True)

        print("teste", teste)
        print(cart.cart_cart.all())

        # self.products = all_products

        self.products = teste
        return cart_product

    class Meta:
        model = CartProducts
        fields = ["product_id", "cart", "product", "storage"]
        read_only_fields = ["cart", "product", "storage"]
        # extra_kwargs = {"user": {"write_only": True}}
