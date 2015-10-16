from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^auth/login', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^auth/refresh', 'rest_framework_jwt.views.refresh_jwt_token'),
    url(r'^auth/verify', 'rest_framework_jwt.views.verify_jwt_token'),

    # APIs
    url(r'^api/users/', include('users.urls')),
    url(r'^api/pods/', include('pods.urls')),
)
