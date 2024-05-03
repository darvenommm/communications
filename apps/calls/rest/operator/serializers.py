from rest_framework import serializers

from calls.models import Operator


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = ("id", "title", "description", "foundation_date")


class OperatorChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = ("title", "description", "foundation_date")
