from django.http import HttpResponse
from django.shortcuts import render
from .forms import RegistrationForm

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def login(request):
    return render(request, "authentication/login.html")

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            #return error message if form is not valid

    return render(request, "authentication/registration.html")

def chat(request):
    return render(request, "interface.html");

def new_group(request):
    return render(request, "newGroup.html");

def search_users(request):
    return render(request, "search_users_friends.html");

def friends(request):
    return render(request, "search_users_friends.html");
