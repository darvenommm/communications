from rest_framework import viewsets

from calls.models import Operator
from .serializers import OperatorDefaultSerializer, OperatorChangeAndUpdateSerializer
from .permisions import OperatorPermission


class OperatorViewSet(viewsets.ModelViewSet):
    queryset = Operator.objects.prefetch_related("subscribers").all()
    permission_classes = (OperatorPermission,)

    def get_serializer_class(self):
        match self.request.method:
            case "POST" | "PUT" | "PATCH":
                self.serializer_class = OperatorChangeAndUpdateSerializer
            case _:
                self.serializer_class = OperatorDefaultSerializer

        return super().get_serializer_class()
