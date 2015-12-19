from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

from .models import Mission

@login_required(login_url='/users/login/')
def manage(request):

    template = loader.get_template('manage.html')
    missions = Mission.objects.all()
    context = RequestContext(request, {
        'missions': missions,
    })
    return HttpResponse(template.render(context))

@login_required(login_url='/users/login/')
def create(request):

    template = loader.get_template('create.html')


    context = RequestContext(request, {
        'missions': "",
    })
    return HttpResponse(template.render(context))
