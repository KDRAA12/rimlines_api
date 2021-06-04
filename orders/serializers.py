from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer

from helpers import CustomSerializer
from orders.models import Product, Order, Payment, LineItem, Refund, Good, Media



class ProductSerializer(CustomSerializer):
    main_image = Base64ImageField(required=True)
    class Meta:
        model=Product
        fields='__all__'
class ShortProductSerializer(CustomSerializer):
    class Meta:
        model = Product
        fields= ['id','title','price']

class ShortGoodSerializer(CustomSerializer):
    class Meta:
        model = Good
        fields =['note','id']

class LineItemSerializer(CustomSerializer):
    product = ShortProductSerializer(read_only=True)
    goods= ShortGoodSerializer(read_only=True,many=True)
    class Meta:
        model=LineItem
        fields='__all__'


class OrderSerializer(CustomSerializer):
    username= serializers.SerializerMethodField()
    items = LineItemSerializer(many=True, read_only=True)

    def get_username(self, obj):
        return f"{obj.owner.user.username}"

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




class RefundSerializer(CustomSerializer):
    class Meta:
        model=Refund
        fields='__all__'
