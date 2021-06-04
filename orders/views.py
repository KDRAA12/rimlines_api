from datetime import datetime, timezone
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
# Create your views here.
from rest_framework.decorators import action
from rest_framework import filters
from rest_framework.response import Response

from helpers import  get_lines_items
from orders.models import Product, Refund, LineItem, Payment, Order, Good, Media
from orders.serializers import ProductSerializer, RefundSerializer, LineItemSerializer, PaymentSerializer, \
    OrderSerializer, GoodSerializer, MediaSerializer

from django_filters.rest_framework import DjangoFilterBackend


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['title']
    search_fields = ['title']

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
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['status']
    ordering = ["-ordered_date"]
    search_fields = ['owner__user__username', 'items__product__title','versed_to']

    def make_payment(self, order):
        if order.owner.edit_balance(order.total_price, "-"):
            p = Payment(amount=order.total_price, order=order, sold_after=order.owner.balance)
            p.save()
            return True
        return False

    def create(self, request, *args, **kwargs):
        if "items" in request.data:
            buffer = get_lines_items(request.data["items"])
            request.data["items"]=[]

        else:
            return Response({"error": "empty orders"})
        _o = OrderSerializer(data=request.data)

        if _o.is_valid():
            order = _o.save()
            order.items.add(*buffer)
            if not self.make_payment(order):
                order.delete()
                return Response({"success": False, "message": "Not enough Balance"})
            goods = []
            for item in order.items.all():
                if item.product.require_manual_activation:
                    print(f"ORDER {order.id} STATUS Require manual activation")
                    order.status = 1
                    _o = OrderSerializer(order)
                    headers = self.get_success_headers(_o.data)
                    return Response(_o.data, status=status.HTTP_201_CREATED, headers=headers)

                gds = Good.objects.filter(product=item.product, status="UNUSED").all()[:item.quantity]

                if not gds:

                    if gds.count() == 0:
                        print("product not in stock")
                    else:
                        print("there is not enough goods")

                    order.status = 0
                    order.save()
                    _o = OrderSerializer(order)
                    headers = self.get_success_headers(_o.data)
                    return Response(_o.data, status=status.HTTP_201_CREATED, headers=headers)
                for good in gds:
                    good.status = "SENT"
                    good.save()
                    goods.append(good.id)
            order.goods.set(goods)
            order.status = 2
            order.save()
            _o = OrderSerializer(order)
            headers = self.get_success_headers(_o.data)
            return Response(_o.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(_o.errors)

    @action(detail=True, methods=['get'])
    def resolve(self, request, pk=None):
        goods = request.data["goods"]
        gds = []
        for gd in goods:
            gd = Good.objects.get(id=gd)
            if gd:
                gd.status = "SENT"
                gd.product.decrement()
                gd.delivery_date = datetime.now()
                gds.append(gd)

        order = Order.objects.get(id=pk)
        order.goods.set(gds)

        order.save()
        o = OrderSerializer(order)
        headers = self.get_success_headers(o.data)
        return Response(o.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def cancel_order(self, request, pk=None):
        pass

#
# class ReportViewSet(viewsets.ModelViewSet):
#     serializer_class = ReportSerializer
#     queryset = Report.objects.all()
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['order', 'level', 'report', 'maker']
#
#     def create(self, request, *args, **kwargs):
#         order = Order.objects.filter(id=self.request.data["order"]).first()
#         l = self.request.data['level'] if self.request.data['level'] else 1
#         report = Report(maker=self.request.user, order=order, message=self.request.data["message"], level=l)
#         report.save()
#         r = ReportSerializer(report)
#         return r.data


class GoodViewSet(viewsets.ModelViewSet):
    serializer_class = GoodSerializer
    queryset = Good.objects.all()

    def create(self, request, *args, **kwargs):
        p = Product.objects.filter(id=self.request.data['product']).first()
        note = self.request.data['note'] if 'note' in request.data else ""
        g = Good(product=p, note=note)
        g.save()
        p.stock += 1
        p.save()
        if "images" in self.request.data:
            for image in self.request.data["images"]:
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

    def retrieve(self, request, pk=None):
        queryset = Good.objects.all()
        good = get_object_or_404(queryset, pk=pk)
        if good.status == "SENT":
            good.status = "OPENED"
            good.opening_date = datetime.now()
            good.save()
        serializer = GoodSerializer(good)
        return Response(serializer.data)


class MediaViewSet(viewsets.ModelViewSet):
    serializer_class = MediaSerializer
    queryset = Media.objects.all()
