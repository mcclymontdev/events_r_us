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
    
    # Creates a list of categories
    CategoryList = forms.ModelChoiceField(queryset = Category.objects.all())

    eventType = forms.ChoiceField(choices= Event.EVENT_TYPES, required=True)
    
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