from rest_framework import serializers
from .models import Product
from rest_framework.validators import UniqueValidator
from categories.serializers import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    def create(self, validated_data):
        category_data = validated_data.pop("category")
        if isinstance(category_data, dict):
            serializer = CategorySerializer(data=category_data)
            serializer.is_valid(raise_exception=True)
            category_new = serializer.save()

            return Product.objects.create(**validated_data, category=category_new)

        return Product.objects.create(**validated_data, category=category_data)

    def update(self, instance: Product, validated_data: dict) -> Product:
        category_data = validated_data.pop("category", None)
        user = validated_data.pop("user", None)
        if category_data and isinstance(category_data, dict):
            serializer = CategorySerializer(data=category_data)
            serializer.is_valid(raise_exception=True)
            category_new = serializer.save()

            instance.category = category_new
            instance.save()
        elif category_data:
            instance.category = category_data
            instance.save()

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = Product
        fields = ["id", "name", "storage", "available", "price", "category", "user"]
        read_only_fields = ["user"]
        extra_kwargs = {
            "name": {
                "validators": [
                    UniqueValidator(
                        queryset=Product.objects.all(),
                        message="Product name already exists",
                    ),
                ]
            },
        }
