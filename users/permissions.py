from rest_framework import permissions
from .models import User


class IsAccounterOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: User):
        return request.user.is_authenticated and obj == request.user
