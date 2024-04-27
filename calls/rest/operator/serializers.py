from rest_framework import serializers

from calls.models import Operator, Subscriber
from auth_users.export.rest import UserReadSerializer


class OperatorReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = ("id", "title", "description", "foundation_date")
        read_only_fields = ("id",)
