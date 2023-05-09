from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CartSerializer
from products.models import Product
from rest_framework.response import Response


class CartProductsView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def create(self, request, *args, **kwargs):
        product = get_object_or_404(
            Product,
            id=self.request.data["product_id"],
        )

        if product.storage == 0:
            return Response({"message": "product is empty in storage"}, 400)
        return super().create(request, *args, **kwargs)
