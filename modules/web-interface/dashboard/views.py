from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.contrib.auth.decorators import login_required
def index(request):
    tib = 'Hello'
    template = loader.get_template('dashboard.html')
    context = RequestContext(request, {
        'tib': tib,
    })
    return HttpResponse(template.render(context))
