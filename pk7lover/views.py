# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext

from accounts.models import Circle
from broadcast.models import Saying


def home(request,show_text=True):
    if request.user.is_authenticated():
        if 'tag' in request.GET and request.GET['tag'] != '1':
            show_text = False
        else:
            sayings = list(Saying.objects.filter(user_id=request.user.id).order_by('time'))
            circle = Circle.objects.get(user_id=request.user.id)
            left_friends = circle.leftright_set.filter(friend_type='left')
            saying_list = [Saying.objects.filter(user_id=lf.friend_id).order_by('time') for lf in left_friends]
            for saying in saying_list:
                sayings.extend(saying)
            sorted(sayings,key=lambda saying:saying.time)
        return render_to_response('index.html',RequestContext(request,locals()))
    else:
        return render_to_response('stranger.html',RequestContext(request,locals()))
