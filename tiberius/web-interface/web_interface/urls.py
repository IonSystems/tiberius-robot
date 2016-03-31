"""web_interface URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from dashboard import views as dashboard_views
import settings
import views

urlpatterns = [
    url(r'^$', dashboard_views.index, name='dashboard'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^control/', include('control.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^missionplanner/', include('missionplanner.urls')),
    url(r'^fleet/', include('fleet.urls')),
]

handler404 = 'web_interface.views.page_not_found'
handler500 = 'web_interface.views.server_error'
if settings.DEBUG:
    urlpatterns += [
        url(r'^404/$', views.page_not_found, name="404"),
        url(r'^500/$', views.server_error, name='500'),
    ]
