from rest_framework import viewsets

from calls.models import Operator
from .serializers import OperatorSerializer, OperatorChangeSerializer
from .permisions import OperatorPermission


class OperatorViewSet(viewsets.ModelViewSet):
    queryset = Operator.objects.prefetch_related("subscribers").all()
    serializer_class = OperatorSerializer
    permission_classes = (OperatorPermission,)

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            self.serializer_class = OperatorChangeSerializer
        else:
            self.serializer_class = OperatorSerializer

        return super().get_serializer_class()
