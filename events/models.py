from django.db import models
import datetime
import django
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.conf import settings

from django.template.defaultfilters import slugify

# Create your models here.
class Category(models.Model):
    Name = models.CharField(max_length=30,primary_key=True)
    class Meta: verbose_name_plural = 'Categories'
    def __str__(self):
        return self.Name

class Event(models.Model):
    NAME_MAX_LENGTH = 100
    DESCRIPTION_MAX_LENGTH = 1250
    ADDRESS_MAX_LENGTH = 100

    EventID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    EventName = models.CharField(max_length=NAME_MAX_LENGTH)
    Description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH)
    Picture = models.ImageField(upload_to='event_image', blank=True)
    
    # Should be requested from API:
    Address = models.CharField(max_length=ADDRESS_MAX_LENGTH)
    Longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    Latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    
    DateTime = models.DateTimeField(default=django.utils.timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Rating = models.IntegerField(default=0)

    EVENT_TYPES = (
        ('One-off','One-off'),
        ('Recurring','Recurring')
    )
    eventType = models.CharField(choices = EVENT_TYPES, max_length=9)

    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.EventName)
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.EventName

class EventRatings(models.Model):
    RatingChoices = [
        (0.5, 0.5),
        (1.0,1.0),
        (1.5,1.5),
        (2.0,2.0),
        (2.5,2.5),
        (3.0,3.0),
        (3.5, 3.5),
        (4.0,4.0),
        (4.5,4.5),
        (5.0,5.0)
    ]

    Rating = models.DecimalField(choices=RatingChoices, max_digits=2, decimal_places=1)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    EventID = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("UserID", "EventID")

    class Meta:
        verbose_name = 'Event ratings'
        verbose_name_plural = 'Event ratings'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    picture = models.ImageField(upload_to='profile_image', blank=True)
    location = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return self.user.Username

class Comment(models.Model):
    CommentID = models.AutoField(primary_key=True)
    EventID = models.ForeignKey(Event, on_delete=models.CASCADE)
    UserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Comment = models.CharField(max_length=200)
    #ParentCommentID = models.ForeignKey(Comments, on_delete=models.CASCADE)
    def __str__(self):
        return self.CommentID 
    
        
        # validates the date ensuring it is not in past 
    def save(self, *args, **kwargs):
        if self.date < datetime.date.today():
            raise ValidationError("The date cannot be in the past!")
            super(Event, self).save(*args, **kwargs)