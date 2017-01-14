from django.conf.urls import url

from api import views


urlpatterns = [
    url(r'^user/$', views.CreateUserAPI.as_view()),
]
