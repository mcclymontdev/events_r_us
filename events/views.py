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

    # TODO: Deal with hidden fields, Address + coords
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('events:index'))
        else:
            print(form.errors)
        
    return render(request, 'events/add_event.html', {'form': form})
