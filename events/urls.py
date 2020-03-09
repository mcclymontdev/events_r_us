from django.urls import path
from events import views

app_name = 'events'

urlpatterns = [
    path('', views.index, name='index'),
    path('sign-up', views.signup, name='sign-up'),
    path('login', views.login, name='login'),
    path('add_event', views.add_event, name='add_event')
]