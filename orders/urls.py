from rest_framework import routers

from orders.views import ProductViewSet, LineItemViewSet, OrderViewSet, PaymentViewSet

router=routers.SimpleRouter()

router.register(r'products',ProductViewSet)
# router.register(r'refunds',RefundViewSet)
router.register(r'lineitems',LineItemViewSet)
router.register(r'orders',OrderViewSet)
router.register(r'payments',PaymentViewSet)

urlpatterns = router.urls

