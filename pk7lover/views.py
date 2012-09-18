# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Circle
from broadcast.models import Saying,PhotoSaying as B_Photo
from albums.models import Gallery,Photo

def home(request,show_text=True):
    if not request.user.is_authenticated():
        return render_to_response('stranger.html',RequestContext(request,locals()))
    
    if not 'p' in request.GET:
        page = 0
    else:
        page = int(request.GET['p'])

    #actives are User object,distinct(filename) just available in
    #postgresql,so mannul...
    acs = Saying.objects.order_by('-pub_date')
    actives = []  #used for display activly users
    for i in range(8):
        for ac in acs:
            if not ac.user in actives:
                actives.append(ac.user)
    try:
        circle = Circle.objects.get(user_id=request.user.id)
    except:
        circle = Circle.objects.create(user_id=request.user.id)
    
    lfs = circle.leftright_set.filter(friend_type='left')
    friends = circle.leftright_set.all()
    neighbours=[]
    for f in friends[:16]:
        if f.friend not in neighbours:
            neighbours.append(f.friend)
       
      
    q_user = Q(user_id = request.user.id) #for retrive syaings,and photo_sayings
    for lf in lfs:
        q_user = q_user | Q(user_id = lf.friend.id) 
  
    if 'tag' in request.GET and request.GET['tag'] != '1':
        show_text = False

        gallerys = Gallery.objects.filter(q_user)
        q_gallery = Q()
        for gallery in gallerys:
            q_gallery = q_gallery | Q(gallery_id = gallery.id)
        
        photos={} #key is every photo_saying,and value is a list of correlation photos
        if len(q_gallery) != 0:
            sum_pages =  B_Photo.objects.filter(q_gallery).order_by('-pub_date').count()
            photosayings = B_Photo.objects.filter(q_gallery).order_by('-pub_date')[page*7:page*7+7]
            for ps in photosayings:
                num = 7 if ps.num > 7 else ps.num
                photos[ps] = Photo.objects.filter(gallery_id=ps.gallery_id).order_by('-upload_date')[:num]
        else:
            sum_pages=0

        pp = page -1
        np = page +1
        sum_pages /= 8

        tag = 2
        return render_to_response('index_photo.html',RequestContext(request,locals()))

    sum_pages = Saying.objects.filter(q_user).order_by('-pub_date').count()
    sayings = Saying.objects.filter(q_user).order_by('-pub_date')[page*14:page*14+13]
    pp = page-1
    np = page+1
    sum_pages /= 14
    
    tag = 1
    return render_to_response('index_text.html',RequestContext(request,locals()))

@csrf_exempt
def browse(request):
   
    page = 1 if not 'p' in request.GET  else int(request.GET['p'])
    sum_pages = Photo.objects.all().count() / 43 + 1
    pp = page-1
    np = page+1
    photos = Photo.objects.all()[(page-1)*43:page*43-1] #(page-1)*31:(page-1)*31+30
    return render_to_response('browse.html',RequestContext(request,locals()))
