from rest_framework import routers

from orders.views import ProductViewSet, LineItemViewSet, OrderViewSet, PaymentViewSet, ReportViewSet

router=routers.SimpleRouter()

router.register(r'products',ProductViewSet)
# router.register(r'refunds',RefundViewSet)
router.register(r'lineitems',LineItemViewSet)
router.register(r'orders',OrderViewSet)
router.register(r'payments',PaymentViewSet)
router.register(r'reports',ReportViewSet)

urlpatterns = router.urls

