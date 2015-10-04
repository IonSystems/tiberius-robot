from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

# Create your views here.
def index(request):
    tib = 'Hello'
    template = loader.get_template('dashboard.html')
    context = RequestContext(request, {
        'tib': tib,
    })
    return HttpResponse(template.render(context))
