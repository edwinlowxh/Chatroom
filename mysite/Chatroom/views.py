from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .forms import RegistrationForm, LoginForm, NewGroupForm, changePasswordForm
from .models import groups, group_members, friend_request, friend, message
import time
import json

# Create your views here.
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

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
            body = json.load(request)

            #Handle sent message
            if (body["function"] == "message"):
                # Create and save message to database
                chat_group = groups.objects.get(id=int(body["group_id"]))
                new_message = message(group = chat_group, sender = request.user, message = body["message"])
                new_message.save()

                # Update last modified time
                # chat_group.last_modified = time.localtime()
                chat_group.save()
                return JsonResponse({}, status = 200)

            #Load message chat window
            if (body["function"] == "messageHistory"):
                # Query for existing messages in group
                query_group = groups.objects.get(id=body["group_id"])
                messages = list(message.objects.filter(group=query_group).values('id',
                                                                                 'group_id',
                                                                                 'sender__id',
                                                                                 'sender__first_name',
                                                                                 'sender__last_name',
                                                                                 'message',
                                                                                 'time'))

                return JsonResponse({"messages": messages}, status=200)

            #Query for users that are not yet added in the group
            if (body["function"] == "users_not_added"):
                group = groups.objects.get(id=body['group_id'])
                members = group_members.objects.all().filter(group=group)
                existing_members = []
                for i in members:
                    existing_members.append(i.member.id)
                new_users = list(User.objects.all().exclude(id__in=existing_members).exclude(is_superuser=True).values('id', 'first_name', 'last_name', 'username'))
                return JsonResponse({"new_users": new_users}, status=200)

            #Add new users to group
            if (body["function"] == "add_users"):
                users_to_add = body["users"]
                group_id = body["group_id"]

                #Save to database
                for id in users_to_add:
                    user = User.objects.get(id = int(id))
                    new_member = group_members(member = user, group = groups.objects.get(id = group_id))
                    new_member.save()

                return JsonResponse({}, status=200)

        #Return chat groups that user is included. Ordered by last message sent
        chat_groups = group_members.objects.filter(member = request.user).order_by("-group__last_modified")
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

        #Get all users excluding admin(/superusers)
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
                    #Check if friend request is existing
                    friendRequest = friend_request.objects.get(requestor=request.user, requestee=User.objects.get(id=user_id))
                except ObjectDoesNotExist:
                    try:
                        #Check if friend request is existing
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

def settings(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = changePasswordForm(request.POST, user=request.user)
            if form.is_valid():
                password = form.cleaned_data['password1']
                print(password)
                user = User.objects.get(id = request.user.id)
                user.set_password(password)
                user.save()

            errors = {'errors': form.errors}
            print(errors)
            return render(request, "settings.html", errors)

        return render(request, "settings.html")
    else:
        return redirect('/Chatroom/login')
