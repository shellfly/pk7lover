from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()

    def __unicode__(self):
        return self.activation_key

    
class Circle(models.Model):
    user = models.OneToOneField(User)
    
    
class Leftright(models.Model):
    TYPE_CHOICE=(('L','left'),('R','right'))
    circle = models.ForeignKey(Circle)
    friend = models.ForeignKey(User)
    friend_type = models.CharField(max_length=5,choices=TYPE_CHOICE)
   
class Personal(models.Model):
    user = models.OneToOneField(User)
    desc = models.TextField(default="")
    tags = models.CharField(default="",max_length=255)
    
