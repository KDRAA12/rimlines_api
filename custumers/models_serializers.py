from rest_framework import serializers

from custumers.models import Customer, Manager
from helpers import CustomSerializer


class CustomerSerializer(CustomSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ManagerSerializer(CustomSerializer):
    class Meta:
        model = Manager
        fields = '__all__'
