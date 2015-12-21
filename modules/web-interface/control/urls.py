from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^send_control_request', views.send_control_request, name='send_control_request'),
]
