from django.conf.urls import url

from . import views
from .models import Mission
from .views import MissionDeleteView
urlpatterns = [
    url(r'^$', views.manage_mission, name='manage_mission'),
    url(r'^create', views.create, name='create'),
    url(r'^manage_tasks', views.manage_tasks, name='manage_tasks'),
    # url(r'^plotting', views.plotting, name='plotting'),
    url(r'^plotting/(?P<id>\d+)/', views.plotting, name='plotting'),
    url(r'^view_mission/(?P<id>\d+)/', views.view_mission, name='view_mission'),
    url(r'^control_panel/(?P<id>\d+)/(?P<platform>\d+)/', views.control_panel, name='control_panel'),
    url(r'^view_task/(?P<id>\d+)/', views.view_task, name='view_task'),
    url(r'^delete_mission/(?P<pk>[\w]+)/$', MissionDeleteView.as_view(
                   model=Mission,
                   success_url='/missionplanner/',
                   template_name='mission_check_delete.html',
                   success_message='Your mission has been deleted successfully.'
                   ), name='delete_mission'),
    url(r'^send_task_request', views.send_task_request,
        name='send_task_request'),
    url(r'^send_nav_request', views.send_nav_request,
        name='send_nav_request'),
]
