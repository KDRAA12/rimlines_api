from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Customer(models.Model):
    CHOICES = (
        ('registered', 'REGISTRED'),
        ('guest', 'GUEST'),
    )
    balance = models.FloatField(default=0)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=300, choices=CHOICES,blank=True,null=True)

    def __str__(self):
        return self.user.username

    def edit_balance(self, amount, opperation):
        if amount.is_digit() and float(amount) > 0:
            if opperation == "+":
                self.balance += float(amount)
            elif opperation == "-":
                self.balance -= float(amount)
            return {'success': True, 'customer': self.save()}
        else:
            return {'success': False}


class Manager(models.Model):
    CHOICES=(
        ('deposit_agent','deposit_agent'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=300, choices=CHOICES, blank=True, null=True)

