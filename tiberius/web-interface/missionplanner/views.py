from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseBadRequest

from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

from .models import Mission
from .models import Task
from .models import MissionObjective
from .models import Waypoint
from .forms import MissionCreateForm

from django.contrib import messages
import json

@login_required(login_url='/users/login/')
def manage(request):

    template = loader.get_template('manage.html')
    missions = Mission.objects.all()
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
        form = MissionCreateForm(request.POST)
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
        form = MissionCreateForm()

    return render(request, 'create.html', {'form': form})

@login_required(login_url='/users/login/')
def plotting(request, id):
    if request.method == 'GET':
        template = loader.get_template('plotting.html')
        context = RequestContext(request, {
            'mission_id': id,
        })
        return HttpResponse(template.render(context))

    if request.method == 'POST':
        waypoints = json.loads(request.POST['waypoints'])
        mission_id = json.loads(request.POST['mission_id'])

        # A few checks to make sure the request is legit.
        if(mission_id != id):
            messages.add_message(request, messages.WARNING,
                                 'Continuity error in request, aborting.')
            return render(request, 'plotting.html', {'form': "meh"})

        mission = Mission.objects.get(pk=mission_id)

        print "Waypoints: " + str(waypoints)
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

            for task_id in item['tasks']:
                # Get the matching task
                task = Task.objects.get(task_id=task_id)

                # Create a mission objective for each waypoint
                objective = MissionObjective(
                    mission=mission,
                    waypoint=waypoint,
                    task=task,
                    order=0)
                objective.save()
                objective_id = objective.id

            # objective.data_to_class(item, mission_id)

        return redirect(request, 'view_mission/' + str(mission_id) + "/", {'request': request.POST})
    else:
        messages.add_message(request, messages.WARNING,
                             'Invalid request, please check.')
        return HttpResponseBadRequest()

@login_required(login_url='/users/login/')
def view_mission(request, id):
    template = loader.get_template('view_mission.html')
    mission = Mission.objects.get(pk=id)
    objectives = MissionObjective.objects.filter(mission=id)
    context = RequestContext(request, {
        'mission': mission,
        'objectives': objectives,
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
        # create a form instance and populate it with data from the request:
        # form = MissionCreateForm(request.POST)
        # # check whether it's valid:
        # if form.is_valid():
        #     # process the data in form.cleaned_data as required
        #     # ...
        #     # redirect to a new URL:
        #     form.save()
        #     return render(request, 'plotting.html', {'form': form})
        #
        # else:
        #     messages.add_message(request, messages.WARNING,
        #                          'Invalid form data, please check.')
        #     return render(request, 'create.html', {'form': form})


# def create(request):
#
#     template = loader.get_template('create.html')
#
#
#     context = RequestContext(request, {
#         'missions': "",
#     })
#     return HttpResponse(template.render(context))
