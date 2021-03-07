from rest_framework import serializers

from alimentation.models import TopUp
from helpers import CustomSerializer


class TopUpSerializer(CustomSerializer):
    title = serializers.CharField(source='get_title')

    class Meta:
        model=TopUp
        fields= '__all__'
        read_only_fields = (
            'title',
        )

