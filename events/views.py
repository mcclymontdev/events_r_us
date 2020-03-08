from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django_registration.views import RegistrationView
from events.forms import UserForm, UserProfileForm

# from .forms import signUpForm
from .models import User

# Create your views here.
def index(request):
    return render(request, 'events/index.html')

def signup(request):

	registered = False
	
	if request.method == 'POST':
		
		user_form = UserForm(request.POST)
		profile_form = UserProfileForm(request.POST)
		
		if user_form.is_valid() and profile_form.is_valid():
		
			user = user_form.save()
			
			user.set_password(user.password)
			
			user.save()
			
			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()
			
			registered = True
			
		else:
			
			print(user_form.errors, profile_form.errors)
			
	else:
		
		user_form = UserForm()
		profile_form = UserProfileForm()
		
	return render(request, 'events/sign-up.html', context = {'user_form': user_form, 'profile_form' : profile_form, 'registered':registered})

def login(request):
    return render(request, 'events/login.html')
    
def user_login(request):
    
    if request.method == 'POST':
        
        username = request.POST.get('username')
        
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            
            if user.is_active:
            
                login(request, user)
                
                return redirect(reverse('1events:index'))
                
            else:
            
                return HttpResponse("Your events account is disabled")
                
        else:
        
            return HttpResponse ("Invalid login credentials")
            
    else:
    
        return render(request, 'events/login.html')

#todo search
#def search(request):
    #return render(request, 'events/base.html')
    
def account(request):
    return render(request, 'events/login.html')