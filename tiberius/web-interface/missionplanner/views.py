from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.utils.safestring import mark_safe
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .models import Mission
from .models import Task
from .models import MissionObjective
from .models import Waypoint
from .models import Robot
from .forms import MissionCreateForm
from .forms import SendTaskRequestForm

from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
import json
from django.core import serializers
import web_interface.settings as settings
import requests
from requests.exceptions import ConnectionError


@login_required(login_url='/users/login/')
def manage_mission(request):

    template = loader.get_template('manage_missions.html')
    missions = Mission.objects.all()
    if not missions:
        messages.add_message(request, messages.INFO,
                             'There are currently no missions to display, create a mission first.')
    context = RequestContext(request, {
        'missions': missions,
    })
    return HttpResponse(template.render(context))


@login_required(login_url='/users/login/')
def manage_tasks(request):
    # Optionally filter the results if a platform parameter is provided
    platform = request.GET.get('platform', -1)
    if platform >= 0:
        tasks = Task.objects.filter(supported_platforms=platform)
    else:
        tasks = Task.objects.all()

    template = loader.get_template('manage_tasks.html')
    form = SendTaskRequestForm()
    context = RequestContext(request, {
        'tasks': tasks,
        'form': form,
    })
    return HttpResponse(template.render(context))


@login_required(login_url='/users/login/')
def create(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MissionCreateForm(request.user, request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            new_mission = form.save()
            mission_id = new_mission.pk
            return redirect(plotting, id=mission_id)

        else:
            messages.add_message(request, messages.WARNING,
                                 'Invalid form data, please check.')
            return render(request, 'create.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MissionCreateForm(request.user)

    return render(request, 'create.html', {'form': form})

@login_required(login_url='/users/login/')
def plotting(request, id):
    # Set template and context for inital view.
    template = loader.get_template('plotting.html')
    json_tasks = json.dumps([task.dict() for task in Task.objects.all()])
    context = RequestContext(request, {
        'mission_id': id,
        'json_tasks': mark_safe(json_tasks),
    })
    # Return the initial view for a GET request.
    if request.method == 'GET':
        return HttpResponse(template.render(context))

    # A POST request is likely to be the plotting button form
    if request.method == 'POST':
        try:
            waypoints = json.loads(request.POST['waypoints'])
            mission_id = int(json.loads(request.POST['mission_id']))
        except ValueError as e:
            # Notify the user that points must be plotted,
            # respond with plotting view.
            messages.add_message(request, messages.WARNING,
                                 'No plots provided!')
            return HttpResponse(template.render(context))

        # A few checks to make sure the request is legit.
        if(mission_id != int(id)):
            messages.add_message(request, messages.WARNING,
                                 'Continuity error in request, aborting.')
            return HttpResponse(template.render(context))

        mission = Mission.objects.get(pk=mission_id)

        print "Waypoints: " + str(waypoints)
        order_counter = 1
        # Iterate through all waypoints
        for item in waypoints:
            print "Item: " + str(item)

            # Create a waypoint for each waypoint in data
            waypoint = Waypoint(
                latitude=item['latLng']['lat'],
                longitude=item['latLng']['lng'],
                altitude=0)
            waypoint.save()
            waypoint_id = waypoint.id

            # Extract all the objectives and save them
            for task_id in item['tasks']:
                # Get the matching task
                task = Task.objects.get(task_id=task_id)

                # Create a mission objective for each waypoint
                objective = MissionObjective(
                    mission=mission,
                    waypoint=waypoint,
                    task=task,
                    order=order_counter)
                objective.save()

            # The waypoint has no tasks, so don't set task the task.
            else:
                # Create a mission objective for each waypoint
                objective = MissionObjective(
                    mission=mission,
                    waypoint=waypoint,
                    order=order_counter)
                objective.save()
            order_counter += 1

            # objective.data_to_class(item, mission_id)
        messages.add_message(request, messages.SUCCESS,
                             'The mission waypoints have been saved!')
        return redirect(mission)
    else:
        messages.add_message(request, messages.WARNING,
                             'Invalid request, please check.')
        return HttpResponseBadRequest()


@login_required(login_url='/users/login/')
def view_mission(request, id):
    template = loader.get_template('view_mission.html')
    mission = Mission.objects.get(pk=id)
    objectives = MissionObjective.objects.filter(mission=id)
    json_objectives = serializers.serialize("json", objectives, use_natural_foreign_keys=True)
    context = RequestContext(request, {
        'mission': mission,
        'objectives': objectives,
        'json_objectives': mark_safe(json_objectives),
    })
    return HttpResponse(template.render(context))


@login_required(login_url='/users/login/')
def control_panel(request, id, platform):
    platform = Robot.objects.get(id=platform)
    template = loader.get_template('control_panel.html')
    mission = Mission.objects.get(pk=id)
    objectives = MissionObjective.objects.filter(mission=id)
    json_objectives = serializers.serialize("json", objectives, use_natural_foreign_keys=True)
    context = RequestContext(request, {
        'mission': mission,
        'objectives': objectives,
        'json_objectives': mark_safe(json_objectives),
        'platform': platform,
    })
    return HttpResponse(template.render(context))


@login_required(login_url='/users/login/')
def view_task(request, id):
    template = loader.get_template('view_task.html')
    task = Task.objects.get(pk=id)
    context = RequestContext(request, {
        'task': task,
    })
    return HttpResponse(template.render(context))


@require_http_methods(["POST"])
def send_task_request(request):
    '''
    Run a singular task on a platform. Call from Ajax.
    '''
    headers = {'X-Auth-Token': settings.SUPER_SECRET_PASSWORD}

    # Extract ID's from form data
    task_id = request.POST.get('task')
    platform_id = request.POST.get('platform')
    command = request.POST.get('command')
    task = Task.objects.get(pk=task_id)
    # We store a seperate task_id that isn't the primary key, so use that.
    task_id = task.task_id

    # Get the ip_address from the platform
    platform = Robot.objects.get(pk=platform_id)
    ip_address = platform.ip_address

    url_start = "http://"
    url_end = ":8000/task"
    url = url_start + ip_address + url_end
    response = ""

    data = {
        'task_id': task_id,
        'ip_address': ip_address,
        'command': command
    }

    try:
        r = requests.post(url,
                          data=data,
                          headers=headers)
        response = r.text
    except ConnectionError as e:
        response = e
    return HttpResponse(response)


@require_http_methods(["POST"])
def send_nav_request(request):
    '''
    Tell Tiberius to navigate to a waypoint. Call from Ajax.
    '''
    headers = {'X-Auth-Token': settings.SUPER_SECRET_PASSWORD}
    
    ip_address = request.POST.get('ip_address')
    url_start = "http://"
    url_end = ":8000/navigation"
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

class MissionDeleteView(DeleteView):
    """
    View to delete a mission, only allows the mission creator to delete mission.
    """
    success_message = "Mission deleted successfully."

    def get_queryset(self):
        qs = super(MissionDeleteView, self).get_queryset()
        return qs.filter(creator=self.request.user)
