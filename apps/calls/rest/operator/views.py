"""Operator view set module."""

from calls.models import Operator
from rest_framework import viewsets

from .permisions import OperatorPermission
from .serializers import OperatorChangeAndUpdateSerializer, OperatorDefaultSerializer


class OperatorViewSet(viewsets.ModelViewSet):
    """Operator view set."""

    queryset = Operator.objects.prefetch_related("subscribers").all()
    permission_classes = (OperatorPermission,)

    def get_serializer_class(self) -> None:
        """Get serializer class.

        Returns:
            None: None.
        """
        match self.request.method:
            case "POST" | "PUT" | "PATCH":
                self.serializer_class = OperatorChangeAndUpdateSerializer
            case _:
                self.serializer_class = OperatorDefaultSerializer

        return super().get_serializer_class()
