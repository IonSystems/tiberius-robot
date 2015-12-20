from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

from .models import Robot

@login_required(login_url='/users/login/')
def list(request):

    template = loader.get_template('list.html')
    fleet = Robot.objects.all()
    context = RequestContext(request, {
        'fleet': fleet,
    })
    return HttpResponse(template.render(context))
