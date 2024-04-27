from rest_framework import viewsets

from calls.models import Operator
from .serializers import OperatorSerializer
from .permisions import OperatorPermission


class OperatorViewSet(viewsets.ModelViewSet):
    queryset = Operator.objects.prefetch_related("subscribers").all()
    serializer_class = OperatorSerializer
    permission_classes = (OperatorPermission,)
