from datetime import datetime

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from rest_framework import serializers, viewsets
# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response

from orders.models import Product, Refund, LineItem, Payment, Order, Report, Good, Media
from orders.serializers import ProductSerializer, RefundSerializer, LineItemSerializer, PaymentSerializer, \
    OrderSerializer, ReportSerializer, GoodSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'], )
    def after(self, request, *args, **kwargs):
        timestamp = int(request.query_params.get('timestamp'))
        print(timestamp)
        date = datetime.fromtimestamp(timestamp / 1e3)
        print(date)
        pds = Product.objects.filter(Q(created_at__gte=date) | Q(updated_at__gte=date)).all()
        product_serialized = ProductSerializer(pds, many=True, context={'request': request})

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

    # filter_backends=[OrderingFilter]
    # ordering=["-ordered_date"]

    @action(detail=True, methods=['get'])
    def add_goods(self, request, pk=None):
        goods = request.data["goods"]
        order = Order.objects.get(pk)
        order.goods = goods
        order.save()
        o = OrderSerializer(order)
        return o.data


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order', 'level', 'report', 'maker']

    def perform_create(self, serializer):
        order = Order.objects.filter(id=self.request.data["order"]).first()
        l = self.request.data['level'] if self.request.data['level'] else 1
        report = Report(maker=self.request.user, order=order, message=self.request.data["message"], level=l)
        report.save()
        r = ReportSerializer(report)
        return r.data


class GoodViewSet(viewsets.ModelViewSet):
    serializer_class = GoodSerializer
    queryset = Good.objects.all()

    def perform_create(self, serializer):

        ims=[]
        if "ims" in self.request.data:
            for image in self.request.data["ims"]:
                i = Media(image=image)
                i.save()
                ims.append(i)
        # is_used=False if 'is_used' not in self.request.data else self.request.data['is_used']
        p=Product.objects.filter(id=self.request.data['product']).first()
        g=Good(product=p,note=self.request.data['note'],is_used=True)
        g.save()
        g.images.set(ims)
        g_s=GoodSerializer(g)
        return g_s.data


