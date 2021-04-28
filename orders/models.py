from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
from custumers.models import Customer
from helpers import alert


class LineItem(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"

    @property
    def get_total_item_price(self):
        return self.quantity * self.product.price

    @property
    def get_total_discount_item_price(self):
        return self.quantity * self.product.discount_price

    @property
    def get_amount_saved(self):
        return self.get_total_item_price - self.get_total_discount_item_price

    @property
    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_item_price
        return self.get_total_item_price


class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    slug = models.SlugField()
    '''to be changed to a default'''
    description = models.TextField()
    main_image = models.ImageField()
    rating = models.FloatField(validators=[MaxValueValidator(5.0), MinValueValidator(0.0)], default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    require_manual_activation = models.BooleanField(default=True)
    stock = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def sale_price(self):
        if self.discount_price:
            return self.discount_price
        else:
            return self.price

    def decrement(self, quantity=1):
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
        if self.stock < 2:
            alert(f"{self.title}", "is out of stock")


class Order(models.Model):
    CHOICES = (
        (-2, 'REQUEST REFUND'),
        (-1, 'REFUND GRANTED'),
        (0, 'PRODUCT NEED RESTOCK'),
        (1, 'AGENT NEEDED FOR ACTIVATION'),
        (2, 'ORDER  COMPLETED'),
    )
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField('LineItem')
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField( choices=CHOICES, blank=True, null=True)
    goods = models.ManyToManyField('good',default=[])

    @property
    def total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price
        return total

    @property
    def total_saved(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_amount_saved()
        return total

    # add a pay order method


class Media(models.Model):
    alt = models.TextField()
    image = models.ImageField(upload_to='goods')


class Good(models.Model):
    CHOICES = (
        ("SENT", "sent"),
        ("OPENED", "opened"),
        ("UNUSED", "unused"),
    )
    images = models.ManyToManyField('Media')
    note = models.TextField(null=True, blank=True)
    product = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True)
    opening_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    adding_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=CHOICES, default="UNUSED", max_length=300)


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
    amount = models.FloatField()
    sold_after = models.FloatField()


class Report(models.Model):
    LEVELS = (
        (0, "MONNEY DIDN'T ARRIVE"),
        (1, "Transaction is incomplete"),
        (2, "false credentials"),
        (3, "to every one")
    )
    maker = models.ForeignKey('custumers.Manager', on_delete=models.CASCADE)
    message = models.TextField()
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, null=True, blank=True)
    level = models.PositiveSmallIntegerField(choices=LEVELS, default=3, )
