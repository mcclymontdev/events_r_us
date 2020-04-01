
from django_registration.forms import RegistrationForm
from django.contrib.auth.models import User
from events.models import User
from events.models import UserProfile, Event, Category, EventRatings, Comment
from django import forms
from django.contrib.auth.forms import UserChangeForm

class UserForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password',)
        
        
class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label='first name; ')
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
        
class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = UserProfilefields = ()

class EventForm(forms.ModelForm):
    EventName = forms.CharField(label='Event name', max_length=Event.NAME_MAX_LENGTH,help_text="Please enter the event name.")
    Description = forms.CharField(label='Description', max_length=Event.DESCRIPTION_MAX_LENGTH,help_text="Please enter a description for the event.", widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    Picture = forms.ImageField(label='Event picture')
    
    DateTime = forms.DateTimeField(label='Date and time',
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    
    # Creates a list of categories
    CategoryList = forms.ModelChoiceField(label='Category', queryset = Category.objects.all())

    eventType = forms.ChoiceField(label='Event type', choices= Event.EVENT_TYPES, required=True)
    
    Address = forms.CharField(label='Address', max_length=Event.ADDRESS_MAX_LENGTH,help_text="Please enter the address of the event.")

    # Handled by API
    Latitude = forms.DecimalField(widget=forms.HiddenInput(), max_digits=22, decimal_places=16)
    Longitude = forms.DecimalField(widget=forms.HiddenInput(), max_digits=22, decimal_places=16)
    
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Event
        fields = ('EventName','Description','Address', 'Picture', 'DateTime', 'CategoryList')

class SearchForm(forms.Form):
    Latitude = forms.DecimalField(widget=forms.HiddenInput(), max_digits=22, decimal_places=16)
    Longitude = forms.DecimalField(widget=forms.HiddenInput(), max_digits=22, decimal_places=16)

    distance = forms.ChoiceField(label="Distance", choices=[("",'Anywhere'), (50,'Within 50 miles'), (100,'Within 100 miles'), (200,'Within 200 miles')], required=False)
    sortBy = forms.ChoiceField(label="Sort by", choices=[('Distance','Distance'), ('Date occuring','Date occuring')], required=False)
    eventType = forms.ChoiceField(label='Event type', choices=[(None,'Any'), ('One-off','One-off'), ('Recurring','Recurring')], required=False)
    category = forms.ModelChoiceField(label='Category', queryset = Category.objects.all(), required=False)
    keywords = forms.CharField( label="Event name", max_length=30, required=False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Any"

class EventRatingsForm(forms.ModelForm):
    rating = forms.DecimalField(widget=forms.RadioSelect(choices=EventRatings.RatingChoices), max_digits=2, decimal_places=1)

    class Meta:
        model = EventRatings
        fields = ('rating',)
        
class CommentForm(forms.ModelForm):
    Comment = forms.CharField(label='', widget = forms.Textarea(attrs = {'class': 'form-control', 'placeholer': 'Comment here', 'rows': 4, 'cols':50}), max_length = Comment.COMMENT_MAX_LENGTH)
    class Meta:
        model = Comment
        fields = ('Comment',)
        
class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email','first_name','last_name',)