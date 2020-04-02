from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django_registration.views import RegistrationView

from events.forms import UserForm, EventForm, SearchForm, EventRatingsForm, ProfileUpdateForm, EditProfileForm, CommentForm
from events.helpers import haversine
from .models import User, Event, Category, EventRatings, Comment

from django.template import RequestContext
from django.template import Context
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm

"""
Simple view to return the index/home page.
"""
def index(request):
    form = SearchForm()
    return render(request, 'events/index.html', {'form' : form})


"""
Simple view to return the about page.
"""
def about(request):
    return render(request, 'events/about.html')

"""
This view allows the user to logout of their account
"""
def user_logout(request):
    logout(request)
    return redirect(reverse('events:index'))
    
"""
This view allows the user to login.
"""
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                auth_login(request, user)
                return redirect(reverse('events:index'))
            else:
                return HttpResponse("Your events account is disabled")
        else:
            print(f"Invalid Login details: {username}, {password}")
            return HttpResponse ("Invalid login credentials")
    else:
        return render(request, 'events/login.html')


"""
This view processes the search logic and passes the relevant results to the template for display.
"""
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
            if category != None:
                query = query.filter(category = category)
            if (eventType != "" and eventType != "Any"):
                query = query.filter(eventType = eventType)

            # Event name keyword search
            if keywords != "":
                for keyword in keywords.split():
                    query = query.filter(EventName__icontains=keyword)

            if sortBy == "Date occuring":
                query = query.order_by('DateTime')

            # For context dictionary
            events = []

            # Calculate distances for each event from the user
            for event in query:
                # Calculate distance between our location and the event location
                haversineDistance = haversine(Latitude, Longitude, event.Latitude, event.Longitude)
                # Filter results by distance if required.
                if withinDistance == "" or haversineDistance < int(withinDistance):
                    event.distance = haversineDistance
                    event.Description = event.Description[:200] + "..."
                    events.append(event)

            # We need to do this filter after calculating the distances
            if sortBy == "Distance":
                events.sort(key=lambda e: e.distance)

            return render(request, 'events/search.html', {'form': form, 'events_list': events})
        else:
            print(form.errors)

    return render(request, 'events/search.html', {'form': form})
    
"""
Allows the user to add a new event.
"""
@login_required
def add_event(request):
    form = EventForm()

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)

        if form.is_valid():
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
                )
            event.save()
            return redirect(reverse('events:index'))
        else:
            print(form.errors)
        
    return render(request, 'events/add_event.html', {'form': form})


"""
This view displays the requested event to the user.
"""
def show_event(request, id, event_slug):
    # Setting up form
    org_eventrating = None
    try:
        org_eventrating = EventRatings.objects.get(EventID=id, UserID=request.user)
        ratingsForm = EventRatingsForm(request.POST or None, initial={'rating':org_eventrating.Rating})
        commentForm = CommentForm(request.POST or None)
    except:
         ratingsForm = EventRatingsForm(request.POST or None)
         commentForm = CommentForm(request.POST or None)

    context_dict = {}
    
    #get comments
    try:
        comments = Comment.objects.filter(EventID = id)
        context_dict['comments'] = comments
    except:
        comments = []
        context_dict['comments'] = None

    # Form handling
    try:
        context_dict['form'] = ratingsForm
        context_dict['event'] = Event.objects.get(EventID=id, slug=event_slug)
        context_dict['commentForm'] = commentForm
        if request.method == 'POST':
            if ratingsForm.is_valid():
                try:
                    eventrating = EventRatings(
                        UserID=request.user, 
                        EventID=context_dict['event'],
                        Rating=ratingsForm.cleaned_data['rating']
                        )
                    eventrating.save()
                except:
                    org_eventrating.Rating = ratingsForm.cleaned_data['rating']
                    org_eventrating.save()
                    
            elif commentForm.is_valid():
                parent_comment = None
                # find the parent, if it exists
                
                
                try:
                    parent_id = int(request.POST.get('parent_id'))
                except:
                    parent_id = None
                    
                # Create the Comment object
                new_comment = commentForm.save(commit = False)
                # Assign the comment to the event
                new_comment.EventID = context_dict['event']
                # Give a local ID to the comment
                new_comment.CommentID = len(comments) + 1
                
                if parent_id:
                    parent_comment = Comment.objects.get(CommentID = parent_id, EventID = new_comment.EventID)
                    # ensure that a parent comment exists
                    if not parent_comment:
                        new_comment.ParentCommentID = None
                    else:
                        # edit the comment to refer to the parent
                        new_comment.Comment = "@" + parent_comment.UserID.username + ' ' + new_comment.Comment
                        # make the parent comment the first comment in the chain
                        while parent_comment.ParentCommentID:
                            parent_comment = parent_comment.ParentCommentID
                        
                        new_comment.ParentCommentID = parent_comment
                    
                else:
                    new_comment.ParentCommentID = None
                
                # Assign comment to logged in user
                new_comment.UserID = request.user
                # Save to database
                new_comment.save()
                return redirect('events:show_event', id=id, event_slug=event_slug)
                
            else:
                print(ratingsForm.errors)
                print(commentForm.errors)

        # Calculating total event rating
        all_ratings = EventRatings.objects.filter(EventID=context_dict['event'])
        num_of_ratings = all_ratings.count()
        if num_of_ratings > 0:                   
            total_rating = 0
            for r in all_ratings:
                total_rating += r.Rating
            context_dict['total_rating'] = round((total_rating/num_of_ratings), 1)
            context_dict['num_of_ratings'] = num_of_ratings
        else:
            context_dict['total_rating'] = 0
            context_dict['num_of_ratings'] = 0

    except Event.DoesNotExist:
        context_dict['event'] = None
        context_dict['form'] = None
        context_dict['commentForm'] = None
        context_dict['comments'] = None



    return render(request, 'events/event.html', context=context_dict)

"""
Displays all of the users events in a grid and allows them to add a new event edit/delete existing events.
"""
@login_required
def manage_events(request):
    context_dict = {}

    try:
        context_dict['events_list'] = Event.objects.filter(UserID=request.user)
    except:
        context_dict['events_list'] = None
    
    return render(request, 'events/manage_events.html', context=context_dict)


"""
Allows the user to edit an existing event.
Modifies an existing event object.
"""
@login_required
def edit_event(request, id):
    try:
        org_event = Event.objects.get(EventID=id, UserID=request.user)
        form = EventForm(request.POST or None, request.FILES or None, instance=org_event, initial={'Latitude':org_event.Latitude, 'Longitude':org_event.Longitude, 'Picture':org_event.Picture})
    except:
        form = None

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('events:show_event', id=id, event_slug=org_event.slug)

    return render(request, 'events/edit_event.html', {'form': form, 'id':id})

"""
Deletes the requested event and displays a message to the user if the deletion was successful or not.
"""
@login_required
def delete_event(request, id):
    context_dict = {}

    try:
        event = Event.objects.get(EventID=id, UserID=request.user)
        context_dict['event'] = event
        event.delete()
        context_dict['status'] = 1
    except:
        context_dict['status'] = 2

    return render(request, 'events/delete_status.html', context_dict)
    
"""
Allows the user to edit their profile details.
"""
@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            return redirect(reverse('events:index'))
    else:
        form = EditProfileForm(instance=request.user)
        args={'form':form}
        return render(request, 'events/profile.html',args)
    
"""
Allows the user to change their account password.
"""
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data = request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('events:index')
            
        else:
            args = {'form':form}
            return render(request, 'events/change_password.html',args)
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request, 'events/change_password.html',args)
    
@login_required
def delete_comment(request, id, event_slug, comment_id):
    context_dict = {}
    context_dict['event'] = Event.objects.get(EventID=id, slug=event_slug)
    try:
        comment = Comment.objects.get(CommentID = comment_id, EventID = context_dict['event'])
        context_dict['comment'] = comment
        #double check the user made the comment
        if request.user == comment.UserID:
            comment.delete()
            context_dict['status'] = 1
        else:
            context_dict['status'] = 3
    
    except:
        context_dict['status'] = 2
        
    

    return render(request, 'events/delete_comment.html', context_dict)
    