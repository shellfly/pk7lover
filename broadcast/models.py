from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from albums.models import Gallery
from activity.models import Activity,Photograph


class Saying(models.Model):
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField(_('pub_date'),default=timezone.now)

    class Meta:
        abstract = True

class PhotoSaying(Saying):
    gallery = models.ForeignKey(Gallery)
    num = models.IntegerField(default=0)
    style = models.CharField(default='1',max_length=1)
    

class ActivitySaying(Saying):
    activity = models.ForeignKey(Activity)
    style = models.CharField(default='2',max_length=1)
    def __unicode__(self):
        return self.activity.name

class PartSaying(Saying):
    activity = models.ForeignKey(Activity)
    work = models.ForeignKey(Photograph)
    style = models.CharField(default='3',max_length=1)
    def __unicode__(self):
        return self.photo.name

