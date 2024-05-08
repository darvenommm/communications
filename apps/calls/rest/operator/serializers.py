from rest_framework import serializers

from calls.models import Operator


class OperatorDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = ("id", "title", "description", "foundation_date")


class OperatorChangeAndUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = ("title", "description", "foundation_date")
