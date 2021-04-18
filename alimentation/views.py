from uuid import uuid5, uuid4
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from alimentation.models import TopUp
from alimentation.serializers import TopUpSerializer
from custumers.models import Customer, Manager
from custumers.models_serializers import CustomerSerializer, ManagerSerializer, UserSerializer


class TopUpViewSet(viewsets.ModelViewSet):
    serializer_class = TopUpSerializer
    queryset = TopUp.objects.all()

    # filter_backends = [OrderingFilter]
    # ordering = ["-ordered_date"]

    def create(self, request):
        print(f"r:{request.data}")
        customer = Customer.objects.filter(user__username=request.data["phone_number"]).first()
        # customer = CustomerSerializer(customer, context={"request": request})
        amount = request.data["amount"]
        if not customer:
            user = User(username=request.data["phone_number"], password=str(uuid4()), is_active=False)
            user.save()
            customer = Customer(user=user)
            customer.save()
        m = Manager.objects.filter(user__username=request.user.username).first()
        print(m.user.username)
        topup = TopUp(maker=m, amount=amount, customer=customer, type="cash")
        topup.save()

        customer.edit_balance(amount=amount, opperation="+")
        print(f"m.user.username {customer.balance}")
        t = TopUpSerializer(topup, context={"request": request})
        return Response({'topup': t.data})

    @action(detail=False, methods=['get'])
    def by_me(self, request, pk=None):
        topups = TopUp.objects.filter(maker__user=request.user.id).all()
        tpups = TopUpSerializer(topups, many=True, context={"request": request})
        return Response(tpups.data)

    @action(detail=False, methods=['get'])
    def un_withdrawed(self, request, pk=None):
        topups = TopUp.objects.filter(withdrawed=False).all()
        tpups = TopUpSerializer(topups, many=True, context={"request": request})
        total = 0
        for topup in topups:
            total += topup.amount
        return Response({"topups": tpups.data, "total": total})

