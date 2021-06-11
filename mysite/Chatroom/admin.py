from django.contrib import admin
from Chatroom.models import groups, group_members

class group_membersInline(admin.TabularInline):
    model = group_members

class group_membersAdmin(admin.ModelAdmin):
    list_display = ('member', 'group')

class groupsAdmin(admin.ModelAdmin):
    inlines = [group_membersInline]

# Register your models here.
admin.site.register(groups, groupsAdmin)
admin.site.register(group_members, group_membersAdmin)
