from django.test import TestCase

# Create your tests here.
from rest_framework.test import force_authenticate, APIRequestFactory
from custumers.models import Manager,Customer,User
from orders.models import Product
factory = APIRequestFactory()
user = User.objects.get(username='olivia')
# view = AccountDetail.as_view()

# Make an authenticated request to the view...
request = factory.get('/accounts/django-superstars/')
force_authenticate(request, user=user)
# response = view(request)