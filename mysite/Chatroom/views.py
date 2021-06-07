from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, LoginForm

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
            else:
                errors = {'errors': form.errors}
                print(errors)
                return render(request, "authentication/login.html", errors)
        else:
            errors = {'errors': form.errors}
            print(errors)
            return render(request, "authentication/login.html", errors)

    return render(request, "authentication/login.html")

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(login)
        else:
            content = {'errors': form.errors}
            return render(request, "authentication/registration.html", content)

    return render(request, "authentication/registration.html")

def chat(request):
    return render(request, "interface.html");

def new_group(request):
    return render(request, "newGroup.html");

def search_users(request):
    return render(request, "search_users_friends.html");

def friends(request):
    return render(request, "search_users_friends.html");
