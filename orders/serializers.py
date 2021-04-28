from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer

from helpers import CustomSerializer
from orders.models import Product, Order, Payment, LineItem, Refund, Report, Good, Media


class ProductSerializer(CustomSerializer):
    main_image = Base64ImageField(required=True)
    class Meta:
        model=Product
        fields='__all__'


class OrderSerializer(CustomSerializer):
    class Meta:
        model=Order
        fields='__all__'


class MediaSerializer(HyperlinkedModelSerializer):
    image= Base64ImageField(required=True)
    class Meta:

        model=Media
        fields=('image','id')


class GoodSerializer(CustomSerializer):
    images = MediaSerializer(many=True, read_only=True)
    class Meta:
        model=Good
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

class ReportSerializer(CustomSerializer):
    class Meta:
        model=Report
        fields='__all__'