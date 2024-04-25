from rest_framework import serializers, viewsets

from calls.models import Operator


class OperatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Operator
        fields = ("id", "title", "description", "foundation_date", "subscribers")


class OperatorViewSet(viewsets.ModelViewSet):
    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer
