from django.contrib import admin
from events.models import Category, Event, Comment, User

from django.contrib.auth.admin import UserAdmin
from .models import User

class EventAdmin(admin.ModelAdmin):
    list_display = ['EventName', 'EventID',]

admin.site.register(Category)
admin.site.register(Event, EventAdmin)
admin.site.register(Comment) 
#admin.site.register(User)