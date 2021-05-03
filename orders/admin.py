from django.contrib import admin

# Register your models here.
from orders.models import Order, Payment, Report, Product, LineItem

admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Report)
admin.site.register(Product)
admin.site.register(LineItem)





