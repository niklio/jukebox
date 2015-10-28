from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

from authentication.views import AccountViewSet
from pods.views import PodViewSet
from songs.views import SongViewSet

router = routers.DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'pods', PodViewSet)
router.register(r'songs', SongViewSet)

urlpatterns = patterns(
    '',
    
    url(r'^admin', include(admin.site.urls)),

    # auth
    url(r'^auth/login/$', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^auth/refresh/$', 'rest_framework_jwt.views.refresh_jwt_token'),
    url(r'^auth/verify/$', 'rest_framework_jwt.views.verify_jwt_token'),

    # APIs
    url(r'^api/', include(router.urls)),
)
