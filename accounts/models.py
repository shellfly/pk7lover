from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()

    def __unicode__(self):
        return self.activation_key

    
class Circle(models.Model):
    user = models.OneToOneField(User)
    def __unicode__(self):
        return self.user.username
    
class Leftright(models.Model):
    TYPE_CHOICE=(('L','left'),('R','right'))
    circle = models.ForeignKey(Circle)
    friend = models.ForeignKey(User)
    group = models.IntegerField(_('group'),default=0)
    friend_type = models.CharField(max_length=5,choices=TYPE_CHOICE)

    def __unicode__(self):
        return self.friend.username
   
class Personal(models.Model):
    user = models.OneToOneField(User)
    desc = models.TextField(_('description'),default="")
    tags = models.CharField(_('tags'),default="",max_length=255)

    def __unicode__(self):
        return self.desc
