from rest_framework import routers

from alimentation.views import TopUpViewSet, VersementViewSet
from orders.views import PaymentViewSet

router =routers.SimpleRouter()

router.register(r't',TopUpViewSet)
router.register(r'versements',VersementViewSet)

urlpatterns = router.urls


