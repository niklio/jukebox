from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter

from accounts.views import AccountViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)

urlpatterns = router.urls