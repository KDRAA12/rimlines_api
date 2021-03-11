
from custumers.models import Customer, Manager,User
from helpers import CustomSerializer


class UserSerializer(CustomSerializer):
    class Meta:
        model = User
        exclude = ('password','user_permissions','groups')


class CustomerSerializer(CustomSerializer):
    user=UserSerializer(many=False, read_only=True)
    class Meta:
        model = Customer
        fields = ['user','balance','status']


class ManagerSerializer(CustomSerializer):
    class Meta:
        model = Manager
        fields = '__all__'


