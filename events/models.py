from django.db import models
import datetime
import django
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    Name = models.CharField(max_length=30,primary_key=True)
    class Meta: verbose_name_plural = 'Categories'
    def __str__(self):
        return self.Name



          
class Event(models.Model):
    EventsID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    EventName = models.CharField(max_length=100)
    Description = models.CharField(max_length=500)
    Picture = models.ImageField(blank=True)
    Address = models.CharField(max_length=100)
    DateTime = models.DateTimeField(default=django.utils.timezone.now)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Rating = models.IntegerField()
    def __str__(self):
        return self.EventName
        

class User(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    UserID = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=30)
    Picture = models.ImageField(upload_to='profile_image', blank=True)
    password = models.CharField(max_length=30, blank=True)
    def __str__(self):
        return self.Username
        
class Comment(models.Model):
    CommentID = models.AutoField(primary_key=True)
    EventID = models.ForeignKey(Event, on_delete=models.CASCADE)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    Comment = models.CharField(max_length=200)
    #ParentCommentID = models.ForeignKey(Comments, on_delete=models.CASCADE)
    def __str__(self):
        return self.CommentID 
    
        
        # validates the date ensuring it is not in past 
    def save(self, *args, **kwargs):
        if self.date < datetime.date.today():
            raise ValidationError("The date cannot be in the past!")
            super(Event, self).save(*args, **kwargs)