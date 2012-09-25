# Create your views here.
from django.http import HttpResponseRedirect,Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Circle
from broadcast.models import Saying,PhotoSaying as B_Photo
from albums.models import Gallery,Photo
from activity.models import Activity
import random

def home(request,show_text=True):
    if not request.user.is_authenticated():
        return render_to_response('stranger.html',RequestContext(request,locals()))
    
    if not 'p' in request.GET:
        page = 0
    else:
        try:
            page = int(request.GET['p'])
        except:
            page = 0

    #actives are User object,distinct(fieldname) only available in
    #postgresql,so mannul...
    acs = B_Photo.objects.order_by('-pub_date')
    actives = []  #used for display activly users
    for ac in acs:
        if not ac.user in actives:
            actives.append(ac.user)
            if len(actives) >= 12:
                break #only show the first 12 people

    try:
        circle = Circle.objects.get(user_id=request.user.id)
    except:
        circle = Circle.objects.create(user_id=request.user.id)
    
    lfs = circle.leftright_set.filter(friend_type='left')
    friends = circle.leftright_set.all()
    friends = [f.friend for f in friends]
    if len(friends) < 10:
        s = 0
    elif len(friends) < 20:
        s = random.randint(0,5)
    else:
        s= random.randint(0,len(friends)-5)
    neighbours=friends[s:s+10]
       
    # all my left-friends and i 
    q_user = Q(user_id = request.user.id) #for retrive syaings,and photo_sayings
    for lf in lfs:
        q_user = q_user | Q(user_id = lf.friend.id) 
  
    # all my leftfriends' gallerys and mine s
    gallerys = Gallery.objects.filter(q_user)
    q_gallery = Q()
    for gallery in gallerys:
        q_gallery = q_gallery | Q(gallery_id = gallery.id)
        
    photos={} #key is every photo_saying,and value is a list of correlation photos
    if len(q_gallery) != 0:
        photosayings = B_Photo.objects.filter(q_gallery).order_by('-pub_date')
        sum_pages = photosayings.count() / 8

        photosayings = photosayings[page*7:page*7+7]
        for ps in photosayings:
            photos[ps] = Photo.objects.filter(gallery_id=ps.gallery_id).order_by('-upload_date')[:7]
    else:
        sum_pages=0

    if page > sum_pages:
        raise Http404()
    
    pp = page-1
    np = page+1

    activities = Activity.objects.order_by('-photo_num')[:4]
    return render_to_response('index_photo.html',RequestContext(request,locals()))

@csrf_exempt
def browse(request):
    page = 1 if not 'p' in request.GET  else int(request.GET['p'])
    sum_pages = Photo.objects.all().count() / 43
    pp = page-1
    np = page+1
    photos = Photo.objects.all()[(page-1)*42:page] #(page-1)*42:(page-1)*42+42
    return render_to_response('browse.html',RequestContext(request,locals()))
