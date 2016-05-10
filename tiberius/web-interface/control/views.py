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
from django.utils.safestring import mark_safe
import json
import web_interface.settings as settings
# Create your views here.


@login_required(login_url='/users/login/')
@ensure_csrf_cookie
def index(request):
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
        tib = Robot.objects.order_by('-pub_date')[:5]
        form = ChangeRobotForm()
        template = loader.get_template('index.html')
        context = RequestContext(request, {
            'tib': tib,
            'form': form
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
        robot_online = check_robot_status(tib.ip_address)
        initial_speed = get_api_param(
            tib.ip_address,
            'motors',
            'get_speed',
            'speed'
        )
        initial_arm_values = get_api_param(
            tib.ip_address,
            'arm',
            'get_speed'
        )

        # If the platform is offline, indicate so with -1
        if isinstance(initial_arm_values, dict):
            initial_arm_speed = mark_safe(initial_arm_values['speed'])
        else:
            initial_arm_speed = -1

        context = RequestContext(request, {
            'ruc': tib,
            'form': form,
            'robot_online': robot_online,
            'initial_speed': mark_safe(initial_speed),
            'initial_arm_values': mark_safe(initial_arm_values),
            'initial_arm_speed': initial_arm_speed
        })
        return HttpResponse(template.render(context))


def get_api_param(ip_address, resource, command, param=None):
    try:
        r = send_command(
                command,
                "http://" + ip_address + ":8000/" + resource)
        if r and param:
            r = json.loads(r)[param]
        elif r:
            r = json.loads(r)
    except KeyError, e:
        return -1
    except TypeError, e:
        return -1
    except ValueError, e:
        return -1
    return r


@require_http_methods(["POST"])
def send_control_request(request):
    '''
        Forward the HTTP request from the browser through to the Tiberius API.
        Handles requests for manual motor control.
    '''
    headers = {'X-Auth-Token': settings.SUPER_SECRET_PASSWORD}

    # Construct url for motor resource on Control API
    ip_address = request.POST.get('ip_address')
    url_start = "http://"
    url_end = ":8000/motors"
    url = url_start + ip_address + url_end
    response = ""

    try:
        r = requests.post(url,
                          data=request.POST.lists(),
                          headers=headers)
        response = r.text
    except ConnectionError as e:
        response = e
    return HttpResponse(response)


@require_http_methods(["POST"])
def send_arm_request(request):
    headers = {'X-Auth-Token': settings.SUPER_SECRET_PASSWORD}

    # Contruct url for motor resource on Control API
    ip_address = request.POST.get('ip_address')
    url_start = "http://"
    url_end = ":8000/arm"
    url = url_start + ip_address + url_end
    response = ""

    try:
        r = requests.post(url,
                          data=request.POST.lists(),
                          headers=headers)
        response = r.text
    except ConnectionError as e:
        response = e
    return HttpResponse(response)


def send_command(command_name, url, headers={'X-Auth-Token': settings.SUPER_SECRET_PASSWORD}):
    try:
        data = {'command': command_name}
        r = requests.post(url,
                          data=data,
                          headers=headers)
        response = r.text
    except ConnectionError as e:
        response = e
    return response


@require_http_methods(["POST"])
def send_task_request(request):
    headers = {'X-Auth-Token': settings.SUPER_SECRET_PASSWORD}

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


def check_robot_status(ip_address):
    url_start = "http://"
    url_end = ":8000/status"
    url = url_start + ip_address + url_end
    headers = {'X-Auth-Token': settings.SUPER_SECRET_PASSWORD}
    data = 'status'
    try:
        r = requests.post(url,
                          data=data,
                          headers=headers)
        status = json.loads(r.text)['connection']
    except ConnectionError as e:
        status = "Offline"
    return status
