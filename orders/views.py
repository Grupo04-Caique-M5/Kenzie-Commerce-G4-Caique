from django.shortcuts import render
from .models import Order
from .serializers import OrderSerializer
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.
class OrderView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = []

    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderDetailView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = []

    serializer_class = []
    queryset = Order.objects.all()

    lookup_url_kwarg = "order_id"
