from rest_framework import serializers, viewsets

from calls.models import Subscriber


class SubscriberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscriber
        fields = ("id", "user", "passport", "birth_date", "operators")


class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
