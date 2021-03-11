from rest_framework import routers

from custumers.views import CustomerViewSet, ManagerViewSet, UserViewSet

router = routers.SimpleRouter()

router.register(r'customers', CustomerViewSet)
router.register(r'managers', ManagerViewSet)
router.register(r'users', UserViewSet)

urlpatterns = router.urls







