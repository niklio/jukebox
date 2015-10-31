from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from authentication.views import AccountViewSet
from pods.views import PodViewSet
from songs.views import SongViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'pods', PodViewSet)
router.register(r'songs', SongViewSet)

accounts_router = NestedSimpleRouter(router, r'accounts', lookup='account')
accounts_router.register('songs', SongViewSet)

pods_router = NestedSimpleRouter(router, r'pods', lookup='pod')
pods_router.register(r'songs', SongViewSet)

urlpatterns = patterns(
    '',
    
    url(r'^admin', include(admin.site.urls)),

    # auth
    url(r'^auth/login/$', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^auth/refresh/$', 'rest_framework_jwt.views.refresh_jwt_token'),
    url(r'^auth/verify/$', 'rest_framework_jwt.views.verify_jwt_token'),

    # APIs
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(accounts_router.urls)),
    url(r'^api/', include(pods_router.urls)),
)
