from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='/users/login/')
def index(request):
    user = request.user
    template = loader.get_template('dashboard.html')
    context = RequestContext(request, {
        'username': user.username,
    })
    return HttpResponse(template.render(context))
