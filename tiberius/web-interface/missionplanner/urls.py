from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.manage, name='manage'),
    url(r'^create', views.create, name='create'),
    url(r'^manage_tasks', views.manage_tasks, name='manage_tasks'),
    # url(r'^plotting', views.plotting, name='plotting'),
    url(r'^plotting/(?P<id>\d+)/', views.plotting, name='plotting'),
    url(r'^view_mission/(?P<id>\d+)/', views.view_mission, name='view_mission'),
    url(r'^view_task/(?P<id>\d+)/', views.view_task, name='view_task'),
]
