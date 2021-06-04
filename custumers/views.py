from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from alimentation.models import TopUp
from custumers.models import Manager, Customer
from custumers.models_serializers import ManagerSerializer, CustomerSerializer, UserSerializer

from django_filters import rest_framework as filters
from rest_framework import filters as filters1

from djangoProject1.filters import ProductFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

    @action(detail=False, methods=['get'])
    def me(self, request, pk=None):
        m = Manager.objects.filter(user=request.user).first()
        mngr = ManagerSerializer(m, context={'request': request})
        return Response(mngr.data)

    @action(detail=True, methods=['get'])
    def balance(self, request, pk=None):
        m = Manager.objects.filter(user__id=pk).first()
        topups = TopUp.objects.filter(maker=m, withdrawed=False).all()

        total = 0
        for topup in topups:
            total += topup.amount

        return Response({'total': total,'count':topups.count()})

    #todo:we should ad away to reterive money from each agent
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    filter_backends = (filters.DjangoFilterBackend,filters1.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ['user__username', 'balance', 'user__first_name','user__last_name']

    @action(detail=True, methods=['get'])
    def me(self, request, pk=None):
        custmer = Customer.objects.filter(user=pk).first()
        c = CustomerSerializer(custmer, context={'request': request})
        return Response(c.data)

