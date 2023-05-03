from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User
from .serializers import UserSerializer
from .permissions import IsAccounterOwner


class UserView(CreateAPIView, UpdateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccounterOwner]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field='pk'

    def get_object(self):
        USERNAME = self.request.user.username
        return self.get_queryset().get(username=USERNAME)
