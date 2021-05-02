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


class Versement(models.Model):

    topups = models.ManyToManyField(TopUp)

    withdrawed_from = models.ForeignKey('custumers.Manager', related_name="versements",null=True,on_delete=models.SET_NULL)
    withdrawed_by = models.ForeignKey('custumers.Manager', related_name="retirements",null=True,on_delete=models.SET_NULL)
    withrdrawed_at = models.DateTimeField(default=datetime.now, blank=True)

    confirmed_by_withdrawer = models.BooleanField(default=False)
    confirmed_by_admin = models.BooleanField(default=False)

    versed_to = models.CharField(max_length=300)
    versed_at = models.DateTimeField(default=datetime.now, blank=True)

    amount_by_withdrawer=models.FloatField(default=datetime.now, blank=True)
    amount_by_admin=models.FloatField(null=True,blank=True)

    note = models.TextField()
    proof =models.ForeignKey('orders.Media',on_delete=models.CASCADE,null=True,blank=True)
