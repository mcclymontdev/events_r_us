from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from events.helpers import haversine

from events.forms import EventForm, SearchForm

# from .forms import signUpForm
from .models import Event, Category

# Create your views here.
def index(request):
    form = SearchForm()
    return render(request, 'events/index.html', {'form' : form})

def signup(request):
    return render(request, 'events/sign-up.html')

def login(request):
    return render(request, 'events/login.html')

def search(request):
    form = SearchForm()

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)

            # Basic search
            Latitude = form.cleaned_data['Latitude']
            Longitude = form.cleaned_data['Longitude']

            # Refined search
            withinDistance = form.cleaned_data['distance']
            sortBy = form.cleaned_data['sortBy']
            eventType = form.cleaned_data['eventType']
            category = form.cleaned_data['category']
            keywords = form.cleaned_data['keywords']

            # TODO: Delete debug prints to decrease database hits
            
            query = Event.objects.all()

            # Filter events based on refined search options
            print("Initial query: " + str(query))
            if category != None:
                query = query.filter(category = category)
                print("category: " + str(query))
            if (eventType != "" and eventType != "Any"):
                query = query.filter(eventType = eventType)
                print("eventType: " + str(query))

            # Event name keyword search
            if keywords != "":
                for keyword in keywords.split():
                    query = query.filter(EventName__icontains=keyword)

            if sortBy == "Date occuring":
                query = query.order_by('DateTime')
                print("sortBy: " + str(query))
            print("Final query: " + str(query))

            # For context dictionary
            events = []

            # Calculate distances for each event from the user
            for event in query:
                # Calculate distance between our location and the event location
                haversineDistance = haversine(Latitude, Longitude, event.Latitude, event.Longitude)
                # Filter results by distance if required.
                if withinDistance == "" or haversineDistance < int(withinDistance):
                    event.distance = haversineDistance
                    events.append(event)

            return render(request, 'events/search.html', {'form': form, 'events_list': events})
        else:
            print(form.errors)

    return render(request, 'events/search.html', {'form': form})
    
def add_event(request):
    form = EventForm()

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)

        if form.is_valid():
            print(form.cleaned_data)
            event = Event(
                UserID=request.user, 
                EventName=form.cleaned_data["EventName"],
                Description=form.cleaned_data["Description"],
                Address=form.cleaned_data["Address"],
                Picture=form.cleaned_data["Picture"],
                Longitude=form.cleaned_data["Longitude"],
                Latitude=form.cleaned_data["Latitude"],
                DateTime=form.cleaned_data["DateTime"],
                category=form.cleaned_data["CategoryList"],
                eventType=form.cleaned_data["eventType"],
                Rating=0,
                )
            event.save()
            return redirect(reverse('events:index'))
        else:
            print(form.errors)
        
    return render(request, 'events/add_event.html', {'form': form})

def show_event(request, id, event_slug):
    context_dict = {}
    try:
        context_dict['event'] = Event.objects.get(EventID=id, slug=event_slug)

    except Event.DoesNotExist:
        context_dict['event'] = None

    return render(request, 'events/event.html', context=context_dict)