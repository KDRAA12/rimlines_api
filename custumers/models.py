from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from helpers import is_number


class Customer(models.Model):
    CHOICES = (
        ('registered', 'REGISTRED'),
        ('guest', 'GUEST'),
    )
    balance = models.FloatField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=300, choices=CHOICES, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def edit_balance(self, amount, opperation):
        if is_number(amount) and float(amount) > 0:
            print("numeric")
            if opperation == "+":
                self.balance += float(amount)
            elif opperation == "-":
                self.balance -= float(amount)
            self.save()
            return {'success': True}
        else:
            print("n")
            return {'success': False}


class Manager(models.Model):
    CHOICES = (
        ('deposit_agent', 'DEPOSIT_AGENT'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=300, choices=CHOICES, blank=True, null=True)
