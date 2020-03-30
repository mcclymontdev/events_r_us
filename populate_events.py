import sys
print("Running directory: " + sys.path[0])

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'events_r_us.settings')

import django
django.setup()

from events.models import Category, Event
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

def populate():
    superusers = [
        {'username':'admin', 'email':'admin@example.com', 'password':'root123', 'first_name':'Admin', 'last_name':''}
    ]

    users = [
        {'username':'Eric1337_Dance', 'email':'Eric1337_Dance@example.com', 'password':'ivorysoap81', 'first_name':'Eric', 'last_name':'Alexander'},
        {'username':'List_UMG', 'email':'Lisa_UMG@example.com', 'password':'murkymonkey72', 'first_name':'Lisa', 'last_name':'Broflovski'},
        {'username':'Steve5013', 'email':'Steve5013@example.com', 'password':'greenjewel20', 'first_name':'Steve', 'last_name':'Jones'},
    ]

    categories = ['Class/Workshop', 'Concert', 'Fitness', 'Entertainment', 'Food', 'Social', 'Trade show', 'Seminar', 'Conference', 'Party']

    for c in categories:
        category = Category.objects.get_or_create(Name=c)
        print("Category added: " + "'" + c + "'")

    for u in superusers:
        user = User.objects.create_superuser(username=u['username'], email=u['email'], password=u['password'], first_name=u['first_name'], last_name=u['last_name'])
        print("Superuser added: " + "'" + u['username'] + "'")

    for u in users:
        user = User.objects.create_user(username=u['username'], email=u['email'], password=u['password'], first_name=u['first_name'], last_name=u['last_name'])
        print("User added: " + "'" + u['username'] + "'")

    # Example event population script
    events = [
        {'username':'Eric1337_Dance', 'EventName':'Dance School', 'Description':'Example description...', 'Picture':'whatever.png', 'Address':'53 Morrison St', 'Latitude':'55.853673', 'Longitude':'-4.268097', 'category':'Fitness','eventType':'Recurring'}
    ]

    for e in events:
        User_obj = User.objects.get(username=e['username'])
        category_obj = Category.objects.get(Name=e['category'])
        event = Event.objects.create(UserID=User_obj, EventName=e['EventName'], Description=e['Description'], Picture=e['Picture'], Address=e['Address'], Latitude=e['Latitude'], Longitude=e['Longitude'], category=category_obj, eventType=e['eventType'])
        print("Event added: " + "'" + e['EventName'] + "'")

if __name__ == '__main__':
    print('Initialising population script...')
    populate()