from rest_framework import serializers

from alimentation.models import TopUp, PendingTopUp
from helpers import CustomSerializer


class TopUpSerializer(CustomSerializer):
    class Meta:
        model=TopUp
        fields= '__all__'


class PendingTopUpSerializer(CustomSerializer):
    class Meta:
        model=PendingTopUp
        fields= '__all__'


