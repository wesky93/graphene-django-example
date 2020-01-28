from django.contrib import admin

from .models import Comment, MeetUp, Place, Topic


# Register your models here.


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    model = Place
    list_display = ('name', 'address',)



class TopicTabularInline(admin.TabularInline):
    model = Topic


@admin.register(MeetUp)
class MeetUpAdmin(admin.ModelAdmin):
    model = MeetUp
    inlines = [
        TopicTabularInline,
    ]
    list_display = ('title', 'description', 'price', 'd_day')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    model = Topic
    list_display = ('meetup', 'title', 'user')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('meetup', 'text', 'user', 'created')
