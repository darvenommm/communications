from rest_framework import serializers, viewsets

from calls.models import OperatorSubscriber


class OperatorSubscriberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OperatorSubscriber
        fields = ("id", "operator", "subscriber")


class OperatorSubscriberViewSet(viewsets.ModelViewSet):
    queryset = OperatorSubscriber.objects.all()
    serializer_class = OperatorSubscriberSerializer
