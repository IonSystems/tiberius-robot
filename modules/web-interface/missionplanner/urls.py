from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.manage, name='manage'),
    url(r'^create', views.create, name='create'),
    url(r'^manage_tasks', views.manage_tasks, name='manage_tasks'),
]
