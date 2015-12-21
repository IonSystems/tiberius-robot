from django.shortcuts import redirect, render
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from users.forms import LoginForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    #TODO: There is probably a proper way of doing this
    return redirect('login')

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

@login_required(login_url='/users/login/')
def logout(request):
    context = RequestContext(request)
    auth.logout(request)
    message = "You have succesfully logged out."
    return render_to_response('logout.html', {"message": message}, context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, "register.html", {
        'form': form,
    })
@login_required(login_url='/users/login/')
def profile(request):
    user = request.user
    context = RequestContext(request)
    return render_to_response('profile.html', {'user' : user}, context)
# def change_password(request):
#     form = ChangePasswordForm()
#     u = User.objects.get(username='john')
#     u.set_password('new password')
#     u.save()
