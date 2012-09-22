from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse,Http404,HttpResponseBadRequest
from django.template.context import RequestContext

from activity.forms import ActivityForm


def create(request):
    if request.method != 'POST':
        form = ActivityForm()
        print form
        return render_to_response('activity/create.html',RequestContext(request,locals()))
    else:
        form = ActivityForm(request.POST)
        return HttpResponse('hello')

def activities(request):
    return render_to_response('activity/activities.html',RequestContext(request,locals()))
    
