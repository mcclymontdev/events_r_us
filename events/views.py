from django.shortcuts import render
from django.http import HttpResponse

from .forms import signUpForm

# Create your views here.
def index(request):
    return render(request, 'events/index.html')

def signup(request):
    form = signUpForm()
    return render(request, 'events/sign-up.html', context={"form" : form})

def login(request):
    return render(request, 'events/login.html')