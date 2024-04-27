from rest_framework import viewsets, permissions

from auth_users.models import User
from .permissions import UserPermission
from .serializers import (
    UserReadSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserDeleteSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, UserPermission)

    def get_serializer_class(self):
        match self.request.method:
            case "POST":
                self.serializer_class = UserCreateSerializer
            case "PUT" | "PATCH":
                self.serializer_class = UserUpdateSerializer
            case "DELETE":
                self.serializer_class = UserDeleteSerializer
            case _:
                self.serializer_class = UserReadSerializer

        return super().get_serializer_class()
