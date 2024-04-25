from rest_framework import serializers, viewsets

from calls.models import SubscriberCall


class SubscriberCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriberCall
        fields = ("id", "caller", "receiver", "start", "duration")
        depth = 2


class SubscriberCallViewSet(viewsets.ModelViewSet):
    queryset = SubscriberCall.objects.all()
    serializer_class = SubscriberCallSerializer
