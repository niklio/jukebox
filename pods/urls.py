from rest_framework.routers import DefaultRouter

from pods.views import PodViewSet

router = DefaultRouter()
router.register('', PodViewSet)

urlpatterns = router.urls