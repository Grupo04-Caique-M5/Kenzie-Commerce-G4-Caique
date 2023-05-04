from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import ProductPermission
from users.serializers import UserSerializer


class ProductView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [ProductPermission]
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        user_serializer = UserSerializer(self.request.user)
        return serializer.save(user_id=user_serializer.data["id"])

    def get_queryset(self):
        name_filter = self.request.query_params.get("name", None)
        category_filter = self.request.query_params.get("category", None)
        print(category_filter)
        if name_filter:
            products_filter = Product.objects.filter(name__iexact=name_filter)
            return products_filter
        if category_filter:
            products_filter = Product.objects.filter(
                category__name__iexact=category_filter
            )
            return products_filter

        return Product.objects.all().order_by("id")


class ProductViewDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [ProductPermission]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
