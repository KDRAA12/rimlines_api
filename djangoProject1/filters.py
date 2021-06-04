from django_filters import rest_framework as filters

from custumers.models import Customer


class ProductFilter(filters.FilterSet):
    balance_gte = filters.NumberFilter(field_name="balance", lookup_expr='gte')
    balance_lte = filters.NumberFilter(field_name="balance", lookup_expr='lte')

    class Meta:
        model = Customer
        fields = ['balance']