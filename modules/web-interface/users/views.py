from django.shortcuts import redirect, render
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from users.forms import LoginForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse

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


def logout(request):
    auth.logout(request)
    return HttpResponse("success")

# def change_password(request):
#     form = ChangePasswordForm()
#     u = User.objects.get(username='john')
#     u.set_password('new password')
#     u.save()
