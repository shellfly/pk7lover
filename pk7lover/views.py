# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext

def home(request):
    if request.user.is_authenticated():
        return render_to_response('index.html',RequestContext(request,locals()))
    else:
        return render_to_response('stranger.html',RequestContext(request,locals()))
