from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from requests.exceptions import ConnectionError
from fleet.models import Robot
from .forms import ChangeRobotForm
import requests
# Create your views here.


@login_required(login_url='/users/login/')
@ensure_csrf_cookie
def index(request):
    tib = Robot.objects.order_by('-pub_date')[:5]
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'tib': tib,
    })
    return HttpResponse(template.render(context))


@login_required(login_url='/users/login/')
@ensure_csrf_cookie
def control(request, id):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ChangeRobotForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            robot_id = form.data.get('name')
            return HttpResponseRedirect('/control/' + robot_id)
        else:
            return HttpResponseRedirect('/invalid form/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ChangeRobotForm()
        template = loader.get_template('control.html')
        tib = Robot.objects.get(id=id)
        context = RequestContext(request, {
            'ruc': tib,
            'form': form
        })
        return HttpResponse(template.render(context))


@require_http_methods(["POST"])
def send_control_request(request):
    headers = {'X-Auth-Token': "supersecretpassword"}

    # Contruct url for motor resource on Control API
    ip_address = request.POST.get('ip_address')
    url_start = "http://"
    url_end = ":8000/motors"
    url = url_start + ip_address + url_end
    response = ""

    if request.POST.get('stop'):
        try:
            data = {'stop': True}
            r = requests.post(url,
                              data=data,
                              headers=headers)
            response = r.text
        except ConnectionError as e:
            response = e
    elif request.POST.get('forward'):
        data = {'forward': True}
        try:
            r = requests.post(url,
                              data=data,
                              headers=headers)
            response = r.text
        except ConnectionError as e:
            response = e
    elif request.POST.get('backward'):
        data = {'backward': True}
        try:
            r = requests.post(url,
                              data=data,
                              headers=headers)
            response = r.text
        except ConnectionError as e:
            response = e

    if request.POST.get('left'):
        data = {'left': True}
        try:
            r = requests.post(url,
                              data=data,
                              headers=headers)
            response = r.text
        except ConnectionError as e:
            response = e
    elif request.POST.get('right'):
        data = {'right': True}
        try:
            r = requests.post(url,
                              data=data,
                              headers=headers)
            response = r.text
        except ConnectionError as e:
            response = e

    if request.POST.get('speed'):
        try:
            data = {'speed': request.POST.get('speed')}
            r = requests.post(url,
                              data=data,
                              headers=headers)
            response = r.text
        except ConnectionError as e:
            response = e
    return HttpResponse(response)


@require_http_methods(["POST"])
def send_task_request(request):
    headers = {'X-Auth-Token': "supersecretpassword"}

    # Contruct url for motor resource on Control API
    ip_address = request.POST.get('ip_address')
    url_start = "http://"
    url_end = ":8000/task"
    url = url_start + ip_address + url_end
    response = ""

    if request.POST.get('command') and request.POST.get('task_id'):
        task_id = request.POST.get('task_id')
        if request.POST.get('command') == "run":
            try:
                data = {'task_id': task_id,
                        'command': 'run'}
                r = requests.post(url,
                                  data=data,
                                  headers=headers)
                response = r.text
            except ConnectionError as e:
                response = e

    return HttpResponse(response)
