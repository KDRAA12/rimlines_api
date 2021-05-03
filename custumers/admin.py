from django.contrib import admin

# Register your models here.
from custumers.models import Customer, Manager

admin.site.register(Manager)
admin.site.register(Customer)




