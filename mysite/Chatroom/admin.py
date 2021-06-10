from django.contrib import admin
from Chatroom.models import groups, group_members

# Register your models here.
admin.site.register(groups)
admin.site.register(group_members)
