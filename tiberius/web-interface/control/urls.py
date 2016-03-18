from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<id>\d+)/', views.control, name='control'),
    url(r'^send_control_request', views.send_control_request,
        name='send_control_request'),
    url(r'^send_task_request', views.send_task_request,
        name='send_task_request'),
]
