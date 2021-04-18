from rest_framework import serializers

from alimentation.models import TopUp
from helpers import CustomSerializer


class TopUpSerializer(CustomSerializer):
    class Meta:
        model=TopUp
        fields= '__all__'

