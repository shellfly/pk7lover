# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.db.models import Q
from django.contrib.auth.models import User

from accounts.models import Circle
from broadcast.models import Saying


def home(request,show_text=True):
    if not request.user.is_authenticated():
        return render_to_response('stranger.html',RequestContext(request,locals()))

    if 'tag' in request.GET and request.GET['tag'] != '1':
        show_text = False
        
    q_user = Q(user_id = request.user.id) #for retrive syaings
    q_gallery = Q() #for retrive photos
    for gallery in Gallery.objects.filter(user_id=request.user.id):
        q_gallery = q_gallery | Q(gallery_id = gallery.id)

    try:
        circle = Circle.objects.get(user_id=request.user.id)
    except:
        pass
    else:
        #friends are LeftRight object
        friends = circle.leftright_set.filter(circle_id=circle.id)
        for lf in circle.leftright_set.filter(friend_type='left'):
            q_user = q_user | Q(user_id = lf.friend.id) 
            for gallery in Gallery.objects.filter(user_id=lf.friend.id):
                q_gallery = q_gallery | Q(gallery_id = gallery.id)
    sayings = Saying.objects.filter(q_user).order_by('-time')
      
    #actives are User object,distinct(filename) just available in postgresql
    acs = Saying.objects.order_by('time').exclude(user=request.user)
    actives = []
    for i in range(8):
        for ac in acs:
            if not ac.user in actives:
                actives.append(ac.user)
        
    return render_to_response('index.html',RequestContext(request,locals()))
        
