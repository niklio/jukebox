from django.conf.urls import patterns, include, url

from users import views

urlpatterns = patterns(
    '',

    url(r'^restricted', views.RestrictedView.as_view()),
)