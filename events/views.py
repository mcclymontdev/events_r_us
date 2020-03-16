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
            print("Location data received successfully!")
            print(form.cleaned_data)
 
            Latitude = form.cleaned_data['Latitude']
            Longitude = form.cleaned_data['Longitude']

            events = []
            all_events = Event.objects.all()
            for event in all_events:
                print(event.EventName)
                event.distance = haversine(Latitude, Longitude, event.Latitude, event.Longitude)
                events.append(event)

            return render(request, 'events/search.html', {'events_list': events})
        else:
            print(form.errors)

    return render(request, 'events/search.html')
    
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