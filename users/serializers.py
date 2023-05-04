from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def create(self, validated_data: dict) -> User:
        if validated_data.get("is_superuser"):
            return User.objects.create_superuser(**validated_data)

        if validated_data.get("is_staff"):
            return User.objects.create_user(**validated_data)

        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        if "is_superuser" in validated_data:
            validated_data.pop("is_superuser")

        instance = super().update(instance, validated_data)

        if validated_data.get("password"):
            instance.set_password(validated_data["password"])

        instance.save()
        return instance

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "name",
            "email",
            "password",
            "is_superuser",
            "is_staff",
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }


class UserActiveSerializer(serializers.ModelSerializer):
    def update(self, instance: User, validated_data: dict) -> User:
        instance.is_active = True
        instance.save()

        return instance

    class Meta:
        model = User
        fields = []
