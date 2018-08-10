from rest_framework import serializers
from .models import Dolar

class DolarSerializer(serializers.Serializer):
    date = serializers.CharField(read_only=True)
    value = serializers.DecimalField(max_digits=7, decimal_places=2)
    usd = serializers.IntegerField()
    UsdToClp = serializers.SerializerMethodField()
    def get_UsdToClp(self, obj):
        return "$" + str("{:,}".format(obj.value*obj.usd))
    def get_usd(self, obj):
        return obj.usd

class ClpSerializer(serializers.Serializer):
    date = serializers.CharField(read_only=True)
    value = serializers.DecimalField(max_digits=7, decimal_places=2)
    clp = serializers.IntegerField()
    ClpToUsd = serializers.SerializerMethodField()
    def get_ClpToUsd(self, obj):
        return "USD " + str("{:,}".format(float(obj.clp / obj.value)))
