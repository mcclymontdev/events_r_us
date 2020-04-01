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
        verbose_name = 'Event ratings'
        verbose_name_plural = 'Event ratings'
        unique_together = ("UserID", "EventID")

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    picture = models.ImageField(upload_to='profile_image', blank=True)
    location = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return self.user.Username

class Comment(models.Model):
    COMMENT_MAX_LENGTH = 200
    CommentID = models.IntegerField(default=1)
    EventID = models.ForeignKey(Event, on_delete=models.CASCADE)
    UserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Comment = models.CharField(max_length = COMMENT_MAX_LENGTH)
    CreatedOn = models.DateTimeField(auto_now_add = True)
    ParentCommentID = models.ForeignKey('self', on_delete=models.CASCADE, null = True, blank = True, related_name = 'replies')
    
    def __str__(self):
        return self.Comment
    
    class Meta:
        ordering = ('CreatedOn',)
        unique_together = ("CommentID", "EventID")
        
    def save(self, *args, **kwargs):
        
        if self._state.adding:
            try:
                LastID = Comment.objects.order_by('CommentID').last().CommentID
            except:
                LastID = None
                
            if LastID is not None:
                CommentID = LastID + 1
        
        super(Comment, self).save(*args, **kwargs)