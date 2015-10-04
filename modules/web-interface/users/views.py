from django.shortcuts import redirect, render
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from users.forms import LoginForm
from django.contrib import auth
from django.http import HttpResponse

# Create your views here.
def index(request):
    tib = 'Hello'
    template = loader.get_template('login.html')
    context = RequestContext(request, {
        'tib': tib,
    })
    return HttpResponse(template.render(context))


def login(request):
    context = RequestContext(request)

    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect('dashboard')
            else:
                form._errors['__all__'] = form.error_class(["Incorrect Username or Password"])

    return render_to_response('login.html', {"form": form}, context)


def logout(request):
    # TODO make logout POST only with js
    if request.method == "POST":
        auth.logout(request)
        return HttpResponse("success")
