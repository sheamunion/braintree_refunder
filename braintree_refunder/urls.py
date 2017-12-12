from django.conf.urls import url
from refunder import views

urlpatterns = [
    url(r'^$', views.new_refund, name='new_refund'),
    url(r'^refund$', views.start_refund, name='start_refund'),
    url(r'^refunding/(?P<file_name>[\w_\-.]+)/$', views.refunding, name='refunding'),
    url(r'^download/(?P<file_name>[\w_\-.]+)/$', views.download, name='download'),
]
