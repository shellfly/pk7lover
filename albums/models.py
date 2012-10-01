from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from albums.signal import user_modify_gallery,user_delete_photo
from django.db.models import F

# Create your models here.

def update_last_modified(sender,gallery,**kwargs):
    '''a signal receiver which updates the update_date for
    the user modify a album
    '''
    print 'signal: update gallery update_date'
    gallery.update_date = timezone.now()
    gallery.save()
    print 'signal:updated'
user_modify_gallery.connect(update_last_modified) 
   
def photo_deleted(sender,gallery,index,**kwargs):
    '''a signal receiver when user delete a photo
    '''
    print 'signal: delete photo'

    if index != gallery.photo_num:
        num = gallery.photo_num
        for i in range(index,num+1):
            gallery.photo_set.filter(index=i).update(index=F('index')-1)

    gallery.photo_num=F('photo_num')-1
    gallery.save()
user_delete_photo.connect(photo_deleted)    
        
class Gallery(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(_('gallery name'),max_length=90)
    desc = models.TextField()
    perm = models.IntegerField(_('permission'),default=0)
    comment = models.BooleanField(_('allow comment'),default=True)
    photo_num = models.BigIntegerField(_('photo number'),default=0)
    cover = models.CharField(_('cover number'),max_length=255,default="")
    create_date = models.DateTimeField(_('date created'),default=timezone.now)
    update_date = models.DateTimeField(_('last updated'),default=timezone.now) 
    
    def __unicode__(self):
        return self.name

class Photo(models.Model):
    gallery = models.ForeignKey(Gallery)
    index = models.IntegerField()
    uname = models.CharField(_('photo name'),max_length=64,default="")
    name = models.CharField(_('photo name'),max_length=64)
    path = models.CharField(_('photo path'),max_length=225)
    thumb128 = models.CharField(_('thumbnail'),max_length=225)
    thumb64 = models.CharField(_('thumbnail2'),max_length=225)
    square = models.CharField(_('square thumb'),max_length=225)
    
    desc = models.CharField(_('description'),max_length=225)
    tags = models.CharField(_('tags'),max_length=256)
    stars = models.IntegerField(_('stars'),default=0)
    upload_date = models.DateTimeField(_('upload date'),default=timezone.now)
    
    def __unicode__(self):
        return self.name
