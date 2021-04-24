from datetime import datetime
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status
# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response

from helpers import decodeDesignImage
from orders.models import Product, Refund, LineItem, Payment, Order, Report, Good, Media
from orders.serializers import ProductSerializer, RefundSerializer, LineItemSerializer, PaymentSerializer, \
    OrderSerializer, ReportSerializer, GoodSerializer, MediaSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'], )
    def after(self, request, *args, **kwargs):
        # todo:add header
        timestamp = int(request.query_params.get('timestamp'))
        date = datetime.fromtimestamp(timestamp / 1e3)
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


class OrderViewSet(viewsets.ModelViewSet):
    # todo:do we make partial order resolving?
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # filter_backends=[OrderingFilter]
    # ordering=["-ordered_date"]

    def make_payment(self, order):
        if order.owner.edit_balance(order.total_price, "-"):
            p = Payment(amount=order.total_price, order=order)
            p.save()
            return True
        return False

    def create(self, request, *args, **kwargs):
        _o = OrderSerializer(data=request.data)
        if _o.is_valid():
            order = _o.save(commit=False)
            if not self.make_payment(order):
                return Response({"success": False, "message": "Not enough Balance"})
            order.save()
            goods = []

            for item in order.items:
                # todo:heavy testing
                gd = Good.objects.filter(product=item.product, product__stock__gte=item.quantity, is_used=False,
                                         product__require_manual_activation=False).all()[:item.quantity]
                if gd:
                    goods.append(gd)
                else:
                    if item.product.require_manual_activation:
                        print("ALERT Agent to resolve it")
                        print("Stock not enough to automaticaly resole order")
                        order.status = 1

                    elif item.product.stock >= item.quantity:
                        print("ALERT ADMIN")
                        print("Stock not enough to automaticaly resole order")

                        order.status = 0

                    elif not Good.objects.filter(product=item.product, is_used=False).all():
                        print("ALERT ADMIN")
                        print("Product not in Stock")

                        order.status = 0

                    order.save()
                    _o = OrderSerializer(order)
                    headers = self.get_success_headers(_o.data)
                    return Response(_o.data, status=status.HTTP_201_CREATED, headers=headers)

            order.goods.set(goods)
            order.status = 2
            order.save()
            _o = OrderSerializer(order)
            headers = self.get_success_headers(_o.data)
            return Response(_o.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def resolve(self, request, pk=None):
        goods = request.data["goods"]
        gds = []
        for gd in goods:
            gd = Good.objects.get(id=gd)
            if gd:
                gds.append(gd)

        order = Order.objects.get(id=pk)
        order.goods.set(gds)
        order.save()
        o = OrderSerializer(order)
        headers = self.get_success_headers(o.data)
        return Response(o.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def cancel_order(self,request,pk=None):
        pass

class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order', 'level', 'report', 'maker']

    def create(self, request, *args, **kwargs):
        order = Order.objects.filter(id=self.request.data["order"]).first()
        l = self.request.data['level'] if self.request.data['level'] else 1
        report = Report(maker=self.request.user, order=order, message=self.request.data["message"], level=l)
        report.save()
        r = ReportSerializer(report)
        return r.data


class GoodViewSet(viewsets.ModelViewSet):
    serializer_class = GoodSerializer
    queryset = Good.objects.all()

    def create(self, request, *args, **kwargs):
        p = Product.objects.filter(id=self.request.data['product']).first()
        is_used = False if 'is_used' not in self.request.data else self.request.data['is_used']
        g = Good(product=p, note=self.request.data['note'], is_used=is_used)
        g.save()
        ims = []
        if "ims" in self.request.data:
            for image in self.request.data["ims"]:
                data = {'image': image, 'alt': 'dd'}
                m = MediaSerializer(data=data)
                if m.is_valid():
                    l = m.save()
                    g.images.add(l.id)
                    g.save()

        g_s = GoodSerializer(g)
        print(g_s.data)
        headers = self.get_success_headers(g_s.data)

        return Response(g_s.data, status=status.HTTP_201_CREATED, headers=headers)


class MediaViewSet(viewsets.ModelViewSet):
    serializer_class = MediaSerializer
    queryset = Media.objects.all()
