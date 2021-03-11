from uuid import uuid5, uuid4

from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from alimentation.models import TopUp
from alimentation.serializers import TopUpSerializer
from custumers.models import Customer, Manager
from custumers.models_serializers import CustomerSerializer, ManagerSerializer, UserSerializer


class TopUpViewSet(viewsets.ModelViewSet):
    serializer_class = TopUpSerializer
    queryset = TopUp.objects.all()


    def create(self, request):
        customer=Customer.objects.filter(user__username=request.data["phone_number"]).first()
        # customer = CustomerSerializer(customer, context={"request": request})
        amount=request.data["amount"]
        if not customer:
            print(customer)
            user=User(username=request.data["phone_number"],password=str(uuid4()),is_active=False)
            user.save()
            customer=Customer(user=user)
            customer.save()
            print(customer)
        print(customer)
        m=Manager.objects.filter(user__username="root").first()
        manager=ManagerSerializer(m,context={'request':request})

        topup=TopUp(maker=m,amount=amount,customer=customer,type="cash")
        topup.save()
        t=TopUpSerializer(topup,context={"request":request})
        return Response({'topup': t.data})


    @action(detail=False, methods=['get'])
    def by_me(self, request,pk=None):
        topups=TopUp.objects.filter(maker__user=request.user.id).all()
        tpups=TopUpSerializer(topups,many=True,context={"request":request})
        return Response(tpups.data)

    @action(detail=False, methods=['get'])
    def un_withdrawed(self, request, pk=None):
        topups = TopUp.objects.filter(withdrawed=False).all()
        tpups = TopUpSerializer(topups, many=True,context={"request":request})
        total=0
        for topup in topups:
            total+=topup.amount

        return Response({"topups":tpups.data,"total":total})
