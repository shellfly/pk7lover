from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
# Create your models here.

class Saying(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(_('saying'),max_length=255)
    time = models.DateTimeField(_('time'),default=timezone.now())
