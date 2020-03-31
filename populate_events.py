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
        {'username':'Lisa_UMG', 'email':'Lisa_UMG@example.com', 'password':'murkymonkey72', 'first_name':'Lisa', 'last_name':'Broflovski'},
        {'username':'Steve5013', 'email':'Steve5013@example.com', 'password':'greenjewel20', 'first_name':'Steve', 'last_name':'Jones'},
        {'username':'karisnimmo99' , 'email': 'karisnimmo1234@example.com', 'password':'joonie94', 'first_name':'Karis', 'last_name':'Nimmo',},
        {'username':'ewanhempsey_skz' , 'email':'ewan_loves_skz@example.com', 'password':'jisung00', 'first_name':'Ewan', 'last_name':'Hempsey',},
        {'username':'rory_comp_genius' , 'email':'rory55@example.com', 'password':'rm567', 'first_name':'Rory', 'last_name':'McClymont',},
        {'username': 'jamesross', 'email':'jamesR_99@example.com', 'password':'bambi90', 'first_name':'James', 'last_name':'Ross',},
        
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
        
        
    event_desc = ['',
    'EricDanceCo is a dance class which involves many different styles of dance including: hiphop, R&B, freestyle, Contemporary and many more. There are difference types of classes ranging from one-to-one tution to group work. ',
    'Learn to rap freestyle with Namjoon. Workshops include individual lessons and group style classes.',
    'Struggling to find a friend to go to a concert with? Use this event to connect with others going to the concert and find friends to go with.',
    'This event showcases many different styles of kpop ranging from BTS, stray kids, ateez, blackpink and many more. If you enjoy kpop this is the party for you!',
    'Need help with procucing your own music and beats? Let the producing team 3Racha help you! This class help you showcase your musical talents and gives you the required skills to create music.',
    'This events help those who struggle to feel motivated while at the gym or working out. Having a trainer or "workout buddy" makes excercising more fun and entertaining.',
    'Every Thursday this club is rented out for those who love raving/ rave music. Enjoy techno beats and find friends with similar music taste. ',
    'Learn how to cook with Chan. Begginner, moderate and expert cooking classes to fill everyones needs.',
    'FixOn is a wood work class for people who are interested in creating and building their own woodwork products.',
    'Love the 80s? This event is perfect for you! 80s themed parties with music food and clothing all from the 80s',
    'Nature lovers who enjoy going walks and hikes, this event gets togther people who enjoy hikes and gives the group a route to follow together. ',
    'If you are interested in architecture this class is perfect for you! Learn all the basics to architecture and begin building your own creations.',
    'Ballet classes taught by the uk best ballet dances. Learn from the best at this class',
    'Kai Dance School are for those who want to learn intricate and high levels of dance.',
    
    ]
    # Example event population script
    events = [
        {'username':'Eric1337_Dance', 'EventName':'EricDanceCo', 'Description':event_desc[0], 'Picture':'dance.png', 'Address':'53 Morrison St', 'Latitude':'55.853673', 'Longitude':'-4.268097', 'category':'Fitness','eventType':'Recurring'},
        {'username':'Lisa_UMG', 'EventName':'Rap Class', 'Description':event_desc[1], 'Picture':'rap.png', 'Address':'7 langley st', 'Latitude':'51.5134', 'Longitude':'-0.1251', 'category':'Class/Workshop','eventType':'Recurring'},
        {'username':'Lisa_UMG', 'EventName':'Concert Buddy', 'Description':event_desc[2], 'Picture':'concertBuddy.png', 'Address':'4 Park Road', 'Latitude':'51.5579', 'Longitude':'0.0840', 'category':'Concert','eventType':'Recurring'},
        {'username':'Lisa_UMG', 'EventName':'Kpop Party', 'Description':event_desc[3], 'Picture':'kpopParty.png', 'Address':'61 Church Street', 'Latitude':'53.3823', 'Longitude':'-1.4713', 'category':'Entertainment','eventType':'Recurring'},
        {'username':'Steve5013', 'EventName':'3Racha', 'Description':event_desc[4], 'Picture':'3racha.png', 'Address':'32 North street', 'Latitude':'53.1288', 'Longitude':'-1.2580', 'category':'Class/Workshop','eventType':'Recurring'},
        {'username':'Steve5013', 'EventName':'workout friends', 'Description':event_desc[5], 'Picture':'workout.png', 'Address':'83 Mayfield Road', 'Latitude':'55.9297', 'Longitude':'-3.1754', 'category':'Fitness','eventType':'Recurring'},
        {'username':'karisnimmo99', 'EventName':'FelixRave', 'Description':event_desc[6], 'Picture':'felixRave.png', 'Address':'17 st. Johns Road', 'Latitude':'55.8414', 'Longitude':'-4.2838', 'category':'Concert','eventType':'Recurring'},
        {'username':'karisnimmo99', 'EventName':'ChansKitchen', 'Description':event_desc[7], 'Picture':'chansKitchen.png', 'Address':'22 School Lane', 'Latitude':'52.5070', 'Longitude':'-0.4122', 'category':'Food','eventType':'Recurring'},
        {'username':'karisnimmo99', 'EventName':'Fix_on', 'Description':event_desc[8], 'Picture':'wood.png', 'Address':'6 Grainge Road', 'Latitude':'50.4036', 'Longitude':'-4.1251', 'category':'Class/Workshop','eventType':'Recurring'},
        {'username':'Lisa_UMG', 'EventName':'80sNight', 'Description':event_desc[9], 'Picture':'80s.png', 'Address':'3 Alexandra Rd', 'Latitude':'52.2354', 'Longitude':'-3.3807', 'category':'Concert','eventType':'Recurring'},
        {'username':'Lisa_UMG', 'EventName':'Hikers', 'Description':event_desc[10], 'Picture':'hike.png', 'Address':'36 West Street', 'Latitude':'53.5233', 'Longitude':'-1.4093', 'category':'Fitness','eventType':'Recurring'},
        {'username':'Lisa_UMG', 'EventName':'Architecture Class', 'Description':event_desc[11], 'Picture':'architecture.png', 'Address':'518 The Green', 'Latitude':'51.4593', 'Longitude':'-3.2121', 'category':'Class/Workshop','eventType':'Recurring'},
        {'username':'Eric1337_Dance', 'EventName':'Ballet Course', 'Description':event_desc[12], 'Picture':'ballet.png', 'Address':'27 Richmond Road', 'Latitude':'52.4785', 'Longitude':'-1.8137', 'category':'Fitness','eventType':'Recurring'},
        {'username':'Eric1337_Dance', 'EventName':'Kai Dance School', 'Description':event_desc[13], 'Picture':'kai.png', 'Address':'56 Kingsway', 'Latitude':'51.4676', 'Longitude':'-0.2753', 'category':'Fitness','eventType':'Recurring'},
        
    ]
    for e in events:
        User_obj = User.objects.get(username=e['username'])
        category_obj = Category.objects.get(Name=e['category'])
        event = Event.objects.create(UserID=User_obj, EventName=e['EventName'], Description=e['Description'], Picture='event_image/'+e['Picture'], Address=e['Address'], Latitude=e['Latitude'], Longitude=e['Longitude'], category=category_obj, eventType=e['eventType'])
        print("Event added: " + "'" + e['EventName'] + "'")

if __name__ == '__main__':
    print('Initialising population script...')
    populate()