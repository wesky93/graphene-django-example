from django.contrib import admin

from .models import Organizer, UserGroup


# Register your models here.


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    model = UserGroup
    list_display = ('name', 'meeting_cycle',)


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    model = Organizer
    list_display = ('name', 'slack_id',)
