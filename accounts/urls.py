from rest_framework.routers import DefaultRouter

from accounts.views import AccountViewSet

router = DefaultRouter()
router.register('', AccountViewSet)

urlpatterns = router.urls