from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

from .models import Mission
from .models import Task
from .forms import MissionCreateForm

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
            return HttpResponseRedirect('/plotting/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MissionCreateForm()

    return render(request, 'create.html', {'form': form})
# def create(request):
#
#     template = loader.get_template('create.html')
#
#
#     context = RequestContext(request, {
#         'missions': "",
#     })
#     return HttpResponse(template.render(context))
