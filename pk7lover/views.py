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
    acs = Saying.objects.order_by('-pub_date')
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
    neighbours=[]
    for f in friends:
        if f.friend not in neighbours:
            neighbours.append(f.friend)
            if len(neighbours) >=12:
                break
       
    # all my left-friends and i 
    q_user = Q(user_id = request.user.id) #for retrive syaings,and photo_sayings
    for lf in lfs:
        q_user = q_user | Q(user_id = lf.friend.id) 
  
    if 'tag' in request.GET and request.GET['tag'] != '1':
        show_text = False

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
        tag = 2
    else:
        sayings = Saying.objects.filter(q_user).order_by('-pub_date')
        sum_pages = sayings.count() / 14

        sayings = sayings[page*13:page*13+13]
        ss = s = []
        for saying in sayings:
            if len(s) == 0 or saying.user_id != s[-1].user_id:
                if len(s) != 0:
                    ss.append(s)
                s = list((saying,))
            else:
                s.append(saying)
        if len(s) != 0: ss.append(s)
        sayings = ss # tranfer to 2-d list,row/ per user
        tag =1

    if page > sum_pages:
        raise Http404()
    template = 'index_text.html' if tag==1 else 'index_photo.html'
    pp = page-1
    np = page+1
    return render_to_response(template,RequestContext(request,locals()))

@csrf_exempt
def browse(request):
    page = 1 if not 'p' in request.GET  else int(request.GET['p'])
    sum_pages = Photo.objects.all().count() / 43
    pp = page-1
    np = page+1
    photos = Photo.objects.all()[(page-1)*42:page] #(page-1)*42:(page-1)*42+42
    return render_to_response('browse.html',RequestContext(request,locals()))
