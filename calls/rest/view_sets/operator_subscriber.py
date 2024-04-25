from rest_framework import serializers, viewsets

from calls.models import OperatorSubscriber


class OperatorSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatorSubscriber
        depth = 1
        fields = "__all__"


class OperatorSubscriberViewSet(viewsets.ModelViewSet):
    queryset = OperatorSubscriber.objects.all()
    serializer_class = OperatorSubscriberSerializer
