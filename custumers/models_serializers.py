from rest_framework import serializers

from custumers.models import Customer, Manager,User
from helpers import CustomSerializer


class UserSerializer(CustomSerializer):
    class Meta:
        model = User
        exclude = ('password','user_permissions','groups')

class CustomerSerializer(CustomSerializer):
    user=UserSerializer(many=False, read_only=True)

    phoneNumber = serializers.SerializerMethodField()

    def get_phoneNumber(self, obj):
        return f"{obj.user.username}"

    class Meta:
        model = Customer
        fields = ['id','user','balance','status','phoneNumber']


class ManagerSerializer(CustomSerializer):
    user = UserSerializer(read_only=True)


    class Meta:
            model = Manager
            fields = ['id','user', 'role']

