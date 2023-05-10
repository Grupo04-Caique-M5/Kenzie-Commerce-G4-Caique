from .models import Order
from .serializers import OrderSerializer, OrderListSerializer
from .permissions import OrderPermission
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from products.models import Product


class OrderView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = OrderListSerializer
    queryset = Order.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        cart = self.request.user.cart

        cart_products = cart.cart_cart.filter(cart=cart).values_list(
            "product", flat=True
        )

        if len(cart_products) == 0:
            return Response({"message": "cart is empty"}, 400)
        new_products = [Product.objects.get(id=product) for product in cart_products]
        count = {}
        for query_product in new_products:
            if query_product.name == query_product.name:
                try:
                    count[query_product.name]
                except KeyError:
                    count[query_product.name] = 0
                for key in count.keys():
                    if key == query_product.name:
                        count[query_product.name] += 1
            if query_product.storage == 0:
                return Response(
                    {"message": "there are no products in the storage"}, 400
                )
        for prod in new_products:
            prod.storage -= count[prod.name]
            prod.save()

        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        user_obj = self.request.user
        self.serializer_class = OrderSerializer

        if user_obj.is_superuser:
            return Order.objects.all()

        if user_obj.is_staff:
            status_filter = self.request.query_params.get("status", None)
            if status_filter:
                order_filter = Order.objects.filter(status__iexact=status_filter)
                orders_list = []
                for order in order_filter:
                    if order.vendor_id == user_obj.id:
                        orders_list.append(order)

                return orders_list
            return Order.objects.filter(vendor_id=user_obj.id)

        return Order.objects.filter(user=user_obj)


class OrderDetailView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [OrderPermission]

    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    lookup_url_kwarg = "order_id"

    def update(self, request, *args, **kwargs):
        if self.request.data.get("status"):
            return super().update(request, *args, **kwargs)

        return Response({"status": "this key is missing"}, 400)
