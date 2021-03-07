from rest_framework import routers

from custumers.views import CustomerViewSet, ManagerViewSet

router = routers.SimpleRouter()

router.register(r'customers', CustomerViewSet)
router.register(r'managers', ManagerViewSet)

urlpatterns = router.urls







