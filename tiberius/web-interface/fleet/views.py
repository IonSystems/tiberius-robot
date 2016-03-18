from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from .models import Robot
from .forms import RobotForm


@login_required(login_url='/users/login/')
def list(request):

    template = loader.get_template('list.html')
    fleet = Robot.objects.all()
    context = RequestContext(request, {
        'fleet': fleet,
    })
    return HttpResponse(template.render(context))


@login_required(login_url='/users/login/')
def modify(request, id):
    robot = Robot.objects.get(id=id)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RobotForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            form.save()
            return render(request, 'index.html')

        else:
            return render(request, 'modify.html', {'form': form, 'robot': robot})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RobotForm(initial=model_to_dict(robot))

    return render(request, 'modify.html', {'form': form, 'robot': robot})


@login_required(login_url='/users/login/')
def view(request, id):

    template = loader.get_template('view.html')
    robot = Robot.objects.get(id=id)
    context = RequestContext(request, {
        'robot': robot,
    })
    return HttpResponse(template.render(context))
