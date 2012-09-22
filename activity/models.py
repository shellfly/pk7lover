from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from albums.models import Photo

# Create your models here.
class Activity(models.Model):
    name = models.CharField(_('activity name'),max_length=128)
    author = models.ForeignKey(User)
    subject = models.TextField(_('subject'))
    beg_date = models.DateTimeField(_('begin date'),default=timezone.now)
    end_date = models.DateTimeField(_('end date'),default=timezone.now)
    tags = models.CharField(_('activity tags'),max_length=64)

class Photograph(Photo):
    activity = models.ForeignKey(Activity)
    vote = models.IntegerField(default=1)
