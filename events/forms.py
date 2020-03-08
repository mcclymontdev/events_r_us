from django_registration.forms import RegistrationForm

from events.models import event

class EventForm(forms.ModelForm):
    EventName = forms.CharField(label='Event name', max_length=event.NAME_MAX_LENGTH,help_text="Please enter the event name.")
    Description = forms.CharField(label='Description', max_length=event.DESCRIPTION_MAX_LENGTH,help_text="Please enter a description for the event.")
    Picture = forms.ImageField(label='Event picture', blank=True)
    
    DateTime = forms.DateTimeField(label='Date and time')
    
    # Should create a dropdown menu of categories?
    Category = forms.ForeignKey(Category)
    
    # Handled by API
    Address = forms.CharField(widget=forms.HiddenInput())
    Longitude = DecimalField(widget=forms.HiddenInput(), max_digits=22, decimal_places=16)
    Latitude = DecimalField(widget=forms.HiddenInput(), max_digits=22, decimal_places=16)
    
    Rating = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    
    # We will need slugs for the event urls
    #slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = event
        #fields = ('EventName','Description','Picture', 'DateTime', 'Category')