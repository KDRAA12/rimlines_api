from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from custumers.models import Manager, Customer
from custumers.models_serializers import ManagerSerializer, CustomerSerializer


class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
