from rest_framework import serializers

from alimentation.models import TopUp
from helpers import CustomSerializer


class TopUpSerializer(CustomSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self,obj):
        return obj.get_title()

    class Meta:
        model=TopUp
        fields= '__all__'

