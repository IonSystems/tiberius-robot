from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^modify/(?P<id>\d+)/', views.modify, name='modify'),
]
