from uuid import uuid5, uuid4
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from alimentation.models import TopUp, Versement
from alimentation.serializers import TopUpSerializer, VersementSerializer
from custumers.models import Customer, Manager
from orders.serializers import MediaSerializer


class TopUpViewSet(viewsets.ModelViewSet):
    serializer_class = TopUpSerializer
    queryset = TopUp.objects.all()

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['maker', 'type','withdrawed']
    ordering = ["-date"]
    search_fields = ['customer__user__username','amount','type']


    def create(self, request):
        customer = Customer.objects.filter(user__username=request.data["phone_number"]).first()
        try:
            amount = int(request.data["amount"])
        except:
            return Response({'error': "amount is not a number"})

        if amount<1:
            return Response({'error': "amount is less than one"})

        if not customer:
            user = User(username=request.data["phone_number"], password=str(uuid4()), is_active=False)
            user.save()
            customer = Customer(user=user)
            customer.save()
        m = Manager.objects.filter(user__username=request.user.username).first()
        topup = TopUp(maker=m, amount=amount, customer=customer, type="cash")
        topup.save()

        customer.edit_balance(amount=amount, opperation="+")
        t = TopUpSerializer(topup, context={"request": request})
        return Response({'topup': t.data})

    # @action(detail=False, methods=['get'])
    # def by_me(self, request, pk=None):
    #     topups = TopUp.objects.filter(maker__user=request.user.id).all()
    #     tpups = TopUpSerializer(topups, many=True, context={"request": request})
    #     return Response(tpups.data)
    #
    # @action(detail=False, methods=['get'])
    # def un_withdrawed(self, request, pk=None):
    #     topups = TopUp.objects.filter(withdrawed=False).all()
    #     tpups = TopUpSerializer(topups, many=True, context={"request": request})
    #     total = 0
    #     for topup in topups:
    #         total += topup.amount
    #     return Response({"topups": tpups.data, "total": total})


class VersementViewSet(viewsets.ModelViewSet):
    queryset = Versement.objects.all()
    serializer_class = VersementSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['confirmed_by_withdrawer', 'confirmed_by_admin']
    ordering = ["-withrdrawed_at"]
    search_fields = ['withdrawed_from__user__username', 'withdrawed_by__user__username', 'amount_by_withdrawer',
                     'amount_by_admin', 'note', 'versed_to']

    def create(self, request):
        topups=request.data['topups']

        tps=[]
        for topup in topups:
            t=get_object_or_404(TopUp,pk=topup)
            t.withdrawed=True
            tps.append(t.id)

        try:
            amount_by_withdrawer = float(request.data["amount_by_withdrawer"])
        except:
            return Response({"success":False,"message":"invalid amount"})

        withdrawed_from=get_object_or_404(Manager,pk=request.data["withdrawed_from"])
        withdrawed_by=get_object_or_404(Manager,pk=request.data["withdrawed_by"])

        data = {'image': request.data['image'], 'alt': ''}
        m = MediaSerializer(data=data)
        if m.is_valid():
            proof = m.save()
        else:
            return Response({"success": False, "message": "invalid Image"})

        v=Versement(withdrawed_from=withdrawed_from,withdrawed_by=withdrawed_by,amount_by_withdrawer=amount_by_withdrawer,note=request.data['note'],confirmed_by_withdrawer=request.data['confirmed_by_withdrawer'],versed_to=request.data['versed_to'],proof=proof)
        v.save()
        v.topups.set(tps)
        v.save()
        v_s=VersementSerializer(v)

        headers = self.get_success_headers(v_s.data)
        return Response(v_s.data, status=status.HTTP_201_CREATED, headers=headers)



