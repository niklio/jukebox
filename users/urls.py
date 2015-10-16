from django.conf.urls import patterns, include, url

from users import views

urlpatterns = patterns(
    '',

    url(r'^register', 'users.views.register'),
    url(r'^login', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^token/refresh', 'rest_framework_jwt.views.refresh_jwt_token'),
    url(r'^token/verify', 'rest_framework_jwt.views.verify_jwt_token'),

    url(r'^$', views.UserProfileList.as_view()),
)