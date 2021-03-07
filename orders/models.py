from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
from custumers.models import Customer


class LineItem(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    @property
    def get_total_item_price(self):
        return self.quantity * self.item.price

    @property
    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    @property
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    @property
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    buying_price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    slug = models.SlugField()
    '''to be changed to a default'''
    description = models.TextField()
    main_image = models.ImageField()
    rating = models.FloatField(validators=[MaxValueValidator(5.0), MinValueValidator(0.0)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def sale_price(self):
        if self.discount_price:
            return self.discount_price
        else:
            return self.price


class Order(models.Model):
    CHOICES = (
        ('refund_requested', 'REFUND_REQUESTED'),
        ('REFUND_GRANTED', 'REFUND_GRANTED'),
        ('pending', 'PENDING'),
        ('Delivered', 'DELIVERED')
    )
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField('LineItem')
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    status = models.CharField(max_length=300, choices=CHOICES, blank=True, null=True)

    @property
    def total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    @property
    def total_saved(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_amount_saved()
        return total

    # add a pay order method


class Refund(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)


class Payment(models.Model):
    def get_amount(self):
        return self.order.total_price

    def get_sold(self):
        return self.customer.sold

    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=get_amount)
    sold_after = models.FloatField(default=get_sold)
