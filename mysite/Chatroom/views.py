from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def login(request):
    return render(request, "authentication/login.html")

def register(request):
    return render(request, "authentication/registration.html")