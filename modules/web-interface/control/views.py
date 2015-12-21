from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from requests.exceptions import ConnectionError
from fleet.models import Robot

import requests
# Create your views here.
@login_required(login_url='/users/login/')
@ensure_csrf_cookie
def index(request):
    tib = Robot.objects.order_by('-pub_date')[:5]
    template = loader.get_template('control.html')
    context = RequestContext(request, {
        'tib': tib,
    })
    return HttpResponse(template.render(context))

@require_http_methods(["POST"])
def send_control_request(request):
    response = ""
    if request.POST.get('stop'):
        try:
            r = requests.get('http://10.113.211.251:8000/motors?stop=True')
            response = r.text
        except ConnectionError:
            response = "ConnectionError"
    if request.POST.get('forward'):
        try:
            r = requests.get('http://10.113.211.251:8000/motors?forward=50')
            response = r.text
        except ConnectionError:
            response = "ConnectionError"
    if request.POST.get('backward'):
        try:
            r = requests.get('http://10.113.211.251:8000/motors?backward=50')
            response = r.text
        except ConnectionError:
            response = "ConnectionError"
    else:
        r = requests.get('http://10.113.211.251:8000/motors?stop=True')
        response = r.text
    return HttpResponse("Done: " + response)
