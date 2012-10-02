# Create your views here.
from django.http import HttpResponseRedirect,Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from accounts.models import Circle
from broadcast.models import PartSaying as B_Part,PhotoSaying as B_Photo,ActivitySaying as B_Activity
from albums.models import Gallery,Photo
from activity.models import Activity
import random

def home(request):

    if not request.user.is_authenticated():
        photos = Photo.objects.all().order_by('?')[:7]
        index = True
        return render_to_response('stranger.html',RequestContext(request,locals()))

    #actives are User object,distinct(fieldname) only available in
    #postgresql,so mannul...
    acs = B_Photo.objects.order_by('-pub_date')
    actives = []  #used for display activly users
    for ac in acs:
        if not ac.user in actives:
            actives.append(ac.user)
            if len(actives) >= 12:
                break #only show the first 12 people

    circle = Circle.objects.get_or_create(user_id=request.user.id)[0]
    friends = circle.leftright_set.all().order_by('?')[:100]
    neighbours =[]
    for f in friends:
        if not f.friend in neighbours:
            neighbours.append(f.friend)
            if len(neighbours) >= 9:
                break
          
    # all my left-friends and i 
    lfs = circle.leftright_set.filter(friend_type='left')
    q_user = Q(user_id = request.user.id) #for retrive syaings,and photo_sayings
    for lf in lfs:
        q_user = q_user | Q(user_id = lf.friend.id) 

    bphotos = B_Photo.objects.filter(q_user).order_by('-pub_date')
    bactivitys = B_Activity.objects.filter(q_user).order_by('-pub_date')
    bparts = B_Part.objects.filter(q_user).order_by('-pub_date')
    sayings = sorted(list(bphotos) + 
                     list(bactivitys) + 
                     list(bparts),
                     key=lambda x:x.pub_date,reverse=True)
    
    paginator = Paginator(sayings,14)
    page = request.GET.get('p')
    try:
        sayings = paginator.page(page)
    except PageNotAnInteger:
        sayings = paginator.page(1)
    except EmptyPage:
        sayings = paginator.page(paginator.num_pages)

    photos = {}
    for saying in sayings :
        if saying.style == '1': #PhotoSaying object,retrieve some extra information
            num = 7 if saying.num > 7 else saying.num
            photos[saying] = Photo.objects.filter(gallery_id=saying.gallery_id).order_by('-upload_date')[:num]

    activities = Activity.objects.filter(end_date__gte=timezone.now()).order_by('-photo_num')[:4]
    return render_to_response('index_photo.html',RequestContext(request,locals()))
