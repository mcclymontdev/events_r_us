from django.contrib import admin
from events.models import Category, Event, Comment, User

admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Comment) 
admin.site.register(User)