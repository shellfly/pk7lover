# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.db.models import Q
from django.contrib.auth.models import User

from accounts.models import Circle
from broadcast.models import Saying,PhotoSaying as B_Photo
from albums.models import Gallery,Photo

def home(request,show_text=True):
    if not request.user.is_authenticated():
        return render_to_response('stranger.html',RequestContext(request,locals()))
    
    #actives are User object,distinct(filename) just available in postgresql
    acs = Saying.objects.order_by('-pub_date')
    actives = []  #used for display active users
    for i in range(8):
        for ac in acs:
            if not ac.user in actives:
                actives.append(ac.user)
    try:
        circle = Circle.objects.get(user_id=request.user.id)
    except:
        circle = Circle.objects.create(user_id=request.user.id)
    finally:
        lfs = circle.leftright_set.filter(friend_type='left')
        friends = circle.leftright_set.all()
        neighbours=[]
        for f in friends:
            if f.friend not in neighbours:
                neighbours.append(f.friend)
       
      
    q_user = Q(user_id = request.user.id) #for retrive syaings,and get updated gallery
    for lf in lfs:
        q_user = q_user | Q(user_id = lf.friend.id) 
  
    if 'tag' in request.GET and request.GET['tag'] != '1':
        show_text = False

        q_gallery = Q()
        gallerys = Gallery.objects.filter(q_user)
        for gallery in gallerys:
            q_gallery = q_gallery | Q(gallery_id = gallery.id)

        photosayings = B_Photo.objects.filter(q_gallery).order_by('-pub_date')
        photos={}
        for ps in photosayings:
            num = 7 and ps.num > 7 or ps.num
            photos[ps] = Photo.objects.filter(gallery_id=ps.gallery_id).order_by('-upload_date')[:num]

        return render_to_response('index_photo.html',RequestContext(request,locals()))

    sayings = Saying.objects.filter(q_user).order_by('-pub_date')
    return render_to_response('index_text.html',RequestContext(request,locals()))



