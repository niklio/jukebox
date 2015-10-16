from django.conf.urls import patterns, include, url

from users import views

urlpatterns = patterns(
    '',
    url(r'^register', 'users.views.register'),
)