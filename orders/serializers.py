from rest_framework import serializers

from helpers import CustomSerializer
from orders.models import Product, Order, Payment, LineItem, Refund


class ProductSerializer(CustomSerializer):
    class Meta:
        model=Product
        fields='__all__'


class OrderSerializer(CustomSerializer):
    class Meta:
        model=Order
        fields='__all__'


class PaymentSerializer(CustomSerializer):
    class Meta:
        model=Payment
        fields='__all__'


class LineItemSerializer(CustomSerializer):
    class Meta:
        model=LineItem
        fields='__all__'


class RefundSerializer(CustomSerializer):
    class Meta:
        model=Refund
        fields='__all__'

