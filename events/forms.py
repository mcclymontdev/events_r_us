from django import forms

from events.models import Event, Category

class EventForm(forms.ModelForm):
    EventName = forms.CharField(label='Event name', max_length=Event.NAME_MAX_LENGTH,help_text="Please enter the event name.")
    Description = forms.CharField(label='Description', max_length=Event.DESCRIPTION_MAX_LENGTH,help_text="Please enter a description for the event.")
    Picture = forms.ImageField(label='Event picture')
    
    DateTime = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    
    # Should create a dropdown menu of categories?
    CategoryList = forms.ModelChoiceField(queryset = Category.objects.all())
    
    Address = forms.CharField(label='Address', max_length=Event.ADDRESS_MAX_LENGTH,help_text="Please enter the address of the event.")

    # Handled by API
    Latitude = forms.DecimalField(widget=forms.HiddenInput(), max_digits=22, decimal_places=16)
    Longitude = forms.DecimalField(widget=forms.HiddenInput(), max_digits=22, decimal_places=16)
    
    # We will need slugs for the event urls
    #slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Event
        fields = ('EventName','Description','Address', 'Picture', 'DateTime', 'CategoryList')