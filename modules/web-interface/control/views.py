from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

from .models import TiberiusRobot
# Create your views here.
@login_required(login_url='/users/login/')
def index(request):
    tib = TiberiusRobot.objects.order_by('-pub_date')[:5]
    template = loader.get_template('control.html')
    context = RequestContext(request, {
        'tib': tib,
    })
    return HttpResponse(template.render(context))
