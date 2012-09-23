from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse,Http404,HttpResponseBadRequest
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required

from activity.forms import ActivityForm
from activity.models import Activity

@login_required
def create(request):
    form = ActivityForm()

    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Activity.objects.create(name=cd['name'],
                                    author=request.user,
                                    subject = cd['subject'],
                                    beg_date = cd['beg_date'],
                                    end_date = cd['end_date'],
                                    tags = cd['tags'])
            return HttpResponse('hello')
    
    return render_to_response('activity/create.html',RequestContext(request,locals()))   


def activities(request):
    return render_to_response('activity/activities.html',RequestContext(request,locals()))
    
