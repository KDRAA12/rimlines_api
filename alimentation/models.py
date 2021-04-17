from datetime import datetime

from django.db import models


# Create your models here.
class TopUp(models.Model):
    CHOICES = (
        ('cash', 'CASH'),
        ('LBOUTIG', 'LBOUTIG'),
    )
    maker = models.ForeignKey('custumers.Manager', on_delete=models.SET_NULL, null=True)
    amount = models.FloatField()
    customer = models.ForeignKey('custumers.Customer', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    type = models.CharField(max_length=300, choices=CHOICES, blank=True, null=True)
    withdrawed = models.BooleanField(default=False)


class PendingTopUp(models.Model):
    Agent = models.ForeignKey('custumers.Manager', on_delete=models.SET_NULL, null=True)
    phone = models.BigIntegerField()
    date = models.DateTimeField()
    Amount = models.FloatField()
    Note = models.TextField()
    status=models.ModelChoiceField
