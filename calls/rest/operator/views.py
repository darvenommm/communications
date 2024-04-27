from rest_framework import permissions, viewsets

from calls.models import Operator
from .serializers import OperatorReadSerializer


class OperatorViewSet(viewsets.ModelViewSet):
    queryset = Operator.objects.prefetch_related("subscribers").all()

    def get_serializer_class(self):
        match self.request.method:
            case _:
                self.serializer_class = OperatorReadSerializer

        return super().get_serializer_class()
