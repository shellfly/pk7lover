from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from albums.models import Gallery
# Create your models here.

class Saying(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(_('saying'),max_length=255)
    pub_date = models.DateTimeField(_('pub_date'),default=timezone.now())

    def __unicode__(self):
        return self.text

class PhotoSaying(models.Model):
    user = models.ForeignKey(User)
    gallery = models.ForeignKey(Gallery)
    num = models.IntegerField(default=0)
    pub_date = models.DateTimeField(_('pub_date'),default=timezone.now())

    def __unicode__(self):
        return self.gallery.name
