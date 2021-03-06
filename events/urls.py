from django.urls import path
from events import views

app_name = 'events'

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('login/', views.login, name='login'),
	path('logout/', views.user_logout, name= 'logout'),
    path('add_event', views.add_event, name='add_event'),
    path('event/<int:id>/<slug:event_slug>/', views.show_event, name='show_event'),
    path('search', views.search, name='search'),
    path('manage_events', views.manage_events, name='manage_events'),
    path('event/<int:id>/edit', views.edit_event, name='edit_event'),
    path('event/<int:id>/delete', views.delete_event, name='delete_event'),
    path('edit_profile', views.edit_profile, name='profile'),
    path('password', views.change_password, name='change_password'),
    path('event/<int:id>/<slug:event_slug>/deletecomment/<int:comment_id>', views.delete_comment, name = 'delete_comment'),
]