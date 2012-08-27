from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from albums.signal import user_modify_gallery

# Create your models here.

def update_last_modified(sender,gallery,**kwargs):
    '''a signal receiver which updates the update_date for
    the user modify a album
    '''
    gallery.update_date = timezone.now()
    gallery.save()
user_modify_gallery.connect(update_last_modified)    
    
class Gallery(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(_('gallery name'),max_length=90)
    description = models.TextField()
    permission = models.IntegerField(_('permission'),default=0)
    comment = models.BooleanField(_('allow comment'),default=True)
    create_date = models.DateTimeField(_('date created'),default=timezone.now)
    update_date = models.DateTimeField(_('last updated'),default=timezone.now) 
    
    def __unicode__(self):
        return self.name
