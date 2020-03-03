from django.shortcuts import render
from django.http import HttpResponse

from django_registration.views import RegistrationView

from .forms import signUpForm
from .models import User

# Create your views here.
def index(request):
    return render(request, 'events/index.html')

class signup(RegistrationView):
    form_class  = "signUpForm"
    def register(self, form):
        """
        Implement user-registration logic here. Access to both the
        request and the registration form is available here.
    
        """
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data["last_name"]
        username = form.cleaned_data["username"]
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password2"]
        picture = form.cleaned_data["picture"]
        location = form.cleaned_data["location"]
        u = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, picture=picture, location=location)
        u.save()

    # https://django-registration.readthedocs.io/en/3.1/quickstart.html#quickstart

def login(request):
    return render(request, 'events/login.html')