# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from albums.models import Photo

# Create your models here.
class Activity(models.Model):
    name = models.CharField(_('activity name'),max_length=128)
    author = models.ForeignKey(User)
    photo_num = models.IntegerField(default=0)
    subject = models.TextField(_('subject'))
    beg_date = models.DateField(_('begin date'),default=timezone.now)
    end_date = models.DateField(_('end date'),default=timezone.now)
    tags = models.CharField(_('activity tags'),max_length=64,help_text="请使用最少的准确的标签,用空格隔开")

    def __unicode__(self):
        return self.name

class Photograph(models.Model):
    activity = models.ForeignKey(Activity)
    author = models.ForeignKey(User)
    index = models.IntegerField(default=0)
    name = models.CharField(_('photo name'),max_length=255)
    path = models.CharField(_('photo path'),max_length=225)
    thumb128 = models.CharField(_('thumbnail'),max_length=225)
    thumb64 = models.CharField(_('thumbnail2'),max_length=225)
    join_date = models.DateTimeField(default=timezone.now)
    votes = models.IntegerField(default=1)

    def __unicode__(self):
        return self.name

class VoteUsers(models.Model):
    activity = models.ForeignKey(Activity)
    user = models.ForeignKey(User)
    voted = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user.username
