from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        if isinstance(data, Category):
            return data
        try:
            category = Category.objects.get(name=data["name"])
            return category

        except Category.DoesNotExist:
            pass

        return super().to_internal_value(data)

    def create(self, validated_data):
        if isinstance(validated_data, Category):
            return validated_data

        return Category.objects.create(**validated_data)

    class Meta:
        model = Category
        fields = "__all__"
