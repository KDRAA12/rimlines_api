from rest_framework import routers

from alimentation.views import TopUpViewSet
from orders.views import PaymentViewSet

router =routers.SimpleRouter()

router.register(r'',TopUpViewSet)

urlpatterns = router.urls


