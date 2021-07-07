from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .forms import RegistrationForm, LoginForm, NewGroupForm
from .models import groups, group_members, friend_request, friend
import json

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
        #Handle message
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
            body = json.load(request)
            print(body["message"])
            return JsonResponse({}, status = 200)

        chat_groups = group_members.objects.filter(member = request.user)
        content = {'chat_groups': chat_groups}
        return render(request, "interface.html", content)
    else:
        return redirect('/Chatroom/login')

def new_group(request):
    if request.user.is_authenticated:
        error = False
        if request.method == "POST":
            form = NewGroupForm(request.POST)
            if form.is_valid():
                group_name = form.cleaned_data['group_name']

                #Create new group in the database
                new_group = groups(group_name = group_name)
                new_group.save()

                #Add members
                for member in form.cleaned_data['users_to_add']:
                    new_member = group_members(member = User.objects.get(id = member), group = groups.objects.get(group_name = group_name))
                    new_member.save()

                #Add self
                new_member = group_members(member = User.objects.get(id = request.user.id), group = groups.objects.get(group_name = group_name))
                new_member.save()
            else:
                #if form is invalid get errors
                print(form.errors)
                error = True;
        users = User.objects.all().exclude(is_superuser = True).exclude(id = request.user.id)
        content = {'Users': users}
        if (error == True):
            #return errors
            content['errors'] = form.errors
        return render(request, "newGroup.html", content);
    else:
        return redirect('/Chatroom/login')

def search_users(request):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
            #Request body
            body = json.load(request)
            user_id = body['user_id']

            #Get user info
            if (body['function'] == "user info"):
                #Query for user using user_id
                try:
                    user = User.objects.get(id = user_id)
                except ObjectDoesNotExist:
                    return JsonResponse(status = 400)
                #Send back
                return JsonResponse({"first_name": user.first_name, "last_name": user.last_name, "email": user.email, "username": user.username, "id": user.id}, status = 200)

            #Add friend
            if (body['function'] == "add friend"):
                #Query for existing friend request
                try:
                    friendRequest = friend_request.objects.get(requestor=request.user, requestee=User.objects.get(id=user_id))
                except ObjectDoesNotExist:
                    try:
                        friendRequest = friend_request.objects.get(requestor=User.objects.get(id=user_id), requestee=request.user)
                    except ObjectDoesNotExist:
                        #Add to model
                        new_request = friend_request(requestor=request.user, requestee=User.objects.get(id=user_id))
                        new_request.save()
                        return JsonResponse({"success": "True", "message": "Friend request sent"},status = 200)

                #If friend request exist return message
                return JsonResponse({"success": "False", "error": "Request already made"}, status = 200)
        else:
            content = {'Users': User.objects.all().exclude(is_superuser = True).exclude(id = request.user.id).values('id', 'username', 'first_name', 'last_name', 'email')}
            #print(content['Users'])
            return render(request, "search_users_friends.html", content);
    else:
        return redirect('/Chatroom/login')


def friends(request):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
            body = json.load(request)

            #Accept/Reject friend request
            if body["function"] == "accept/reject":
                if body["choice"] == "accept":
                    newFriend = friend(initiator=User.objects.get(id=body["user_id"]), receiver=request.user)
                    newFriend.save()

                #Delete regardless accept or reject
                friend_request.objects.filter(requestor=User.objects.get(id=body["user_id"]), requestee=request.user).delete()

                return JsonResponse({"success": "true"}, status=200)

            #Get user info
            elif body["function"] == "user info":
                #Query for user using user_id
                try:
                    user = User.objects.get(id = body["user_id"])
                except ObjectDoesNotExist:
                    return JsonResponse(status = 400)
                #Send back
                return JsonResponse({"first_name": user.first_name, "last_name": user.last_name, "email": user.email, "username": user.username, "id": user.id}, status = 200)

        #Get friend requests and friends
        friendRequests = friend_request.objects.filter(requestee=request.user)
        friends = friend.objects.filter(Q(initiator=request.user ) | Q(receiver=request.user))
        content = {"friendRequests": friendRequests, "friends": friends}
        return render(request, "search_users_friends.html", content)
    else:
        return redirect('/Chatroom/login')
