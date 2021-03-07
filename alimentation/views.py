from uuid import uuid5

from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from alimentation.models import TopUp
from alimentation.serializers import TopUpSerializer
from custumers.models import Customer


class TopUpViewSet(viewsets.ModelViewSet):
    serializer_class = TopUpSerializer
    queryset = TopUp.objects.all()

    def perform_create(self, serializer):
        customer=Customer.objects.filter(user__username=self.request['username']).first()
        if not customer:
            user=User(username=self.request['username'],password=str(uuid5()),is_active=False)
            user.save()
            customer=Customer(user=user,status='registered')
            customer.save()

        customer.edit_balance(self.request['amount'],"+")
        return customer





