from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from events.forms import EventForm

# from .forms import signUpForm
from .models import Event, Category

# Create your views here.
def index(request):
    return render(request, 'events/index.html')

def signup(request):
    return render(request, 'events/sign-up.html')

def login(request):
    return render(request, 'events/login.html')

def search(request):
    return render(request, 'events/base.html')
    
def add_event(request):
    form = EventForm()

    # TODO: Implement saving image upload.
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
