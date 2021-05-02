from rest_framework import serializers

from alimentation.models import TopUp, Versement
from helpers import CustomSerializer


class TopUpSerializer(CustomSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return f"{obj.customer.user.username}"

    class Meta:
        model=TopUp
        # fields=['customer',,'maker','amount','type','withdrawed','date']
        fields='__all__'

class VersementSerializer(CustomSerializer):
    class Meta:
        model=Versement
        fields= '__all__'

