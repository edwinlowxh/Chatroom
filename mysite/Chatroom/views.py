from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def _login(request):
    if request.user.is_authenticated:
        return redirect(chat)
    else:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    return redirect(chat)
                else:
                    form.add_error('password', 'Invalid Password')
            errors = {'errors': form.errors}
            print(errors)
            return render(request, "authentication/login.html", errors)

    return render(request, "authentication/login.html")

def _logout(request):
    logout(request)
    return redirect('/Chatroom/login')

def register(request):
    if request.user.is_authenticated:
        return redirect(chat)
    else:
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(_login)
            else:
                content = {'errors': form.errors}
                return render(request, "authentication/registration.html", content)

    return render(request, "authentication/registration.html")

def chat(request):
    if request.user.is_authenticated:
        return render(request, "interface.html");
    else:
        return redirect('/Chatroom/login')

def new_group(request):
    if request.user.is_authenticated:
        users = User.objects.all().exclude(is_superuser = True)
        content = {'Users': users}
        return render(request, "newGroup.html", content);
    else:
        return redirect('/Chatroom/login')

def search_users(request):
    return render(request, "search_users_friends.html");

def friends(request):
    return render(request, "search_users_friends.html");
