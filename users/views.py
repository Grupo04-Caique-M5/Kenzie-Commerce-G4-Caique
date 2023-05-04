from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User
from .serializers import UserSerializer, UserActiveSerializer
from .permissions import IsAccounterOwner


class UserView(CreateAPIView, UpdateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccounterOwner]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"

    def get_object(self):
        USERNAME = self.request.user.username
        return self.get_queryset().get(username=USERNAME)


class UserDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    lookup_url_kwarg = "user_id"

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class UserActiveView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = User.objects.all()
    serializer_class = UserActiveSerializer

    lookup_url_kwarg = "user_id"
