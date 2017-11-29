from django.conf.urls import url
from refunder import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^refunding$', views.refunding),
]
