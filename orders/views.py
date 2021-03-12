from datetime import datetime

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from rest_framework import serializers, viewsets
# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response

from orders.models import Product, Refund, LineItem, Payment, Order
from orders.serializers import ProductSerializer, RefundSerializer, LineItemSerializer, PaymentSerializer, \
    OrderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'],)
    def after(self, request, pk=None):
        timestamp=request.data['timestamp']
        date = datetime.datetime.fromtimestamp(timestamp / 1e3)
        products=Product.objects.filter(Q(created_at__gte=date) | Q(created_at__gte=date)).all()
        product_serialized=ProductSerializer(products,many=True)

        return Response(product_serialized.data)


#
# class RefundViewSet(serializers.ModelSerializer):
#     queryset=Refund.objects.all()
#     serializer_class=RefundSerializer
#
#     def perform_create(self, serializer):
#         order = get_object_or_404(Order, self.request.data['order'])
#         status = order.owner.edit_balance(order.total_price, "+")
#         if status["success"] == True:
#             refund = Refund(order=order,refund=)
#             payment.save()
#             return payment
#         else:
#             return Response(status)
#

class LineItemViewSet(viewsets.ModelViewSet):
    queryset = LineItem.objects.all()
    serializer_class = LineItemSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        order = get_object_or_404(Order, self.request.data['order'])
        status = order.owner.edit_balance(order.total_price, "-")
        if status["success"] == True:
            payment = Payment(order=order)
            payment.save()
            return payment
        else:
            return Response(status)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
