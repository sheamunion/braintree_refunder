from django.conf.urls import url
from refunder import views

urlpatterns = [
    url(r'^$', views.new_refund, name='new_refund'),
    url(r'^refund$', views.start_refund, name='start_refund'),
    url(r'^refunding$', views.refunding, name='refunding'),
]
