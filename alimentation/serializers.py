from rest_framework import serializers

from alimentation.models import TopUp, Versement
from helpers import CustomSerializer


class TopUpSerializer(CustomSerializer):
    class Meta:
        model=TopUp
        fields= '__all__'


class VersementSerializer(CustomSerializer):
    class Meta:
        model=Versement
        fields= '__all__'

