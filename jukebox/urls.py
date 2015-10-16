from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),

    # APIs
    url(r'^api/users/', include('users.urls')),
    url(r'^api/pods/', include('pods.urls')),
)
