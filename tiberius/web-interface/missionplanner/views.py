from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.utils.safestring import mark_safe
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

from .models import Mission
from .models import Task
from .models import MissionObjective
from .models import Waypoint
from .forms import MissionCreateForm

from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
import json

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

    template = loader.get_template('manage_tasks.html')
    tasks = Task.objects.all()
    context = RequestContext(request, {
        'tasks': tasks,
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
    json_waypoints = json.dumps([ob.waypoint.dict() for ob in objectives])
    print json_waypoints
    context = RequestContext(request, {
        'mission': mission,
        'objectives': objectives,
        'json_waypoints': mark_safe(json_waypoints),
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


class MissionDeleteView(DeleteView):
    """
    View to delete a mission, only allows the mission creator to delete mission.
    """
    success_message = "Mission deleted successfully."

    def get_queryset(self):
        qs = super(MissionDeleteView, self).get_queryset()
        return qs.filter(creator=self.request.user)
