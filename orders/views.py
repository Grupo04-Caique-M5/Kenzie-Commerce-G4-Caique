from .models import Order
from .serializers import OrderSerializer, OrderListSerializer
from .permissions import OrderPermission
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response


class OrderView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = OrderListSerializer
    queryset = Order.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user_obj = self.request.user
        self.serializer_class = OrderSerializer

        if user_obj.is_superuser:
            return Order.objects.all()
            
        if user_obj.is_staff:
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
        
        return Response(
            {"status": "this key is missing"},
            400
        )
