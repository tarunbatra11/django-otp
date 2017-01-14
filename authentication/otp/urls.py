from django.conf.urls import include, url
from django.contrib import admin

from otp import views


urlpatterns = [
    url(r'^getcode/$', views.generate_code),
    url(r'^verifycode/$', views.verify_code),
]
