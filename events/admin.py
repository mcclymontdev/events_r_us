from django.contrib import admin
from events.models import Category, Event, Comment, EventRatings

from django.contrib.auth.admin import UserAdmin
from .models import User

class EventAdmin(admin.ModelAdmin):
    list_display = ['EventName', 'EventID',]
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ['CommentID', 'EventID', 'UserID','Comment']
    list_filer = ['EventID', 'UserID']

admin.site.register(Category)
admin.site.register(Event, EventAdmin)
admin.site.register(Comment) 
admin.site.register(EventRatings)