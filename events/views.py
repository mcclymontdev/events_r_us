from django.shortcuts import render
from django.http import HttpResponse

from events.forms import EventForm

# from .forms import signUpForm
from .models import User

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

    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect(reverse('events:add_event'))
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)
        
    return render(request, 'events/add_event.html', {'form': form})
