from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import TiberiusRobot
# Create your views here.
def index(request):
    tib = TiberiusRobot.objects.order_by('-pub_date')[:5]
    template = loader.get_template('web_interface/index.html')
    context = RequestContext(request, {
        'tib': tib,
    })
    return HttpResponse(template.render(context))
