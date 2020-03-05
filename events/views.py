from django.shortcuts import render
from django.http import HttpResponse

from django_registration.views import RegistrationView

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