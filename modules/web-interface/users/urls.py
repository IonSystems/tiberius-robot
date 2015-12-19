from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile', views.profile, name='profile'),
    url(r'^login', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^register$', views.register, name='register'),
    url('^change_password/', auth_views.password_change, {'template_name': 'change_password.html'}),
    url('^password_change_done/', auth_views.password_change_done, name='password_change_done'),

]
