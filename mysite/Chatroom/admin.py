from django.contrib import admin
from Chatroom.models import groups, group_members, friend_request, friend, message

class group_membersInline(admin.TabularInline):
    model = group_members

class group_membersAdmin(admin.ModelAdmin):
    list_display = ('member', 'group')

class groupsAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_name')
    inlines = [group_membersInline]

class friend_requestAdmin(admin.ModelAdmin):
    list_display = ('requestor', 'requestee')

class friendAdmin(admin.ModelAdmin):
    list_display = ('initiator', 'receiver')

class messageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'group', 'message', 'time')

# Register your models here.
admin.site.register(groups, groupsAdmin)
admin.site.register(group_members, group_membersAdmin)
admin.site.register(friend_request, friend_requestAdmin)
admin.site.register(friend, friendAdmin)
admin.site.register(message, messageAdmin)
