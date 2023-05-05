from django.shortcuts import render
from rest_framework import generics
from users.serializers import UserSerializer
from .serializers import OrderSerializer
from .models import Order
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class OrdersView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def perform_create(self, serializer):
        # user_serializer = UserSerializer()
        return serializer.save(user=self.request.user)
