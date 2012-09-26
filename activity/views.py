# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse,Http404,HttpResponseBadRequest
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import F
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from activity.forms import ActivityForm
from activity.models import Activity,Photograph,VoteUsers
from broadcast.models import ActivitySaying,PartSaying

from pk7lover.settings import MEDIA_ROOT,MEDIA_URL
import os
import random
from PIL import Image

@login_required
def create(request):
    form = ActivityForm()

    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ac = Activity.objects.create(
                name=cd['name'],
                author=request.user,
                subject = cd['subject'],
                beg_date = cd['beg_date'],
                end_date = cd['end_date'],
                tags = cd['tags'])
            ActivitySaying.objects.create(
                user = request.user,
                activity = ac,
                pub_date = timezone.now())
            return HttpResponseRedirect(reverse('7activity',args=[ac.id]))
    return render_to_response('activity/create.html',RequestContext(request,locals()))   

def activity(request,activity_id):
    id = int(activity_id)
    activity = get_object_or_404(Activity,id=id)
    photos = Photograph.objects.filter(activity_id=id).order_by('-join_date')
    
    authors=[photo.author for photo in photos]
    if request.user in authors:
        participanted = True
    
    if activity.end_date < timezone.now().date():
        exceed = True
    photos = photos[:12]
    authors = authors[:12]
    f7 = Photograph.objects.filter(activity_id=id).order_by('-votes')[:7]
    return render_to_response('activity/activity.html',RequestContext(request,locals()))

def activities(request,t=0):
    if t != 0 and t != 1:
        raise Http404()

    news = Activity.objects.all().order_by('-beg_date')[:7]
    if int(t) == 0:
        activities = Activity.objects.filter(end_date__gte = timezone.now()).order_by('-photo_num')
    else:
        phs = Photograph.objects.filter(author=request.user).order_by('-join_date')
        activities = [ph.activity for ph in phs]
        mine = True

    paginator = Paginator(activities,7)
    page = request.GET.get('p')
    try:
        activities = paginator.page(page)
    except PageNotAnInteger:
        activities = paginator.page(1)
    except EmptyPage:
        activities = paginator.page(paginator.num_pages)
        
    photos={}
    for activity in activities:
        photos[activity] = Photograph.objects.filter(activity_id=activity.id)[:7]

    return render_to_response('activity/activities.html',RequestContext(request,locals()))
    
def allwork(request,activity_id):
    activity = get_object_or_404(Activity,id=activity_id)
    photos = Photograph.objects.filter(activity_id=activity.id)

    page = 1 if not 'p' in request.GET  else int(request.GET['p'])
    sum_pages = photos.count() / 43
    pp,np = page-1,page+1
    photos = photos[(page-1)*42:page*42]
    return render_to_response('activity/allwork.html',RequestContext(request,locals()))

@login_required
def delete(request,activity_id):
    activity = get_object_or_404(Activity,id=activity_id)
    if  request.user.id !=activity.author.id:
        raise Http404()
    
    activity.delete()
    return HttpResponseRedirect(reverse('7people',args=[request.user.username]))

@login_required
def vote(request,id):
    ph = get_object_or_404(Photograph,id=id)
    people = ph.author
    activity = ph.activity
    voteusers = VoteUsers.objects.filter(ph = ph)
    voteusers = [vu.user for vu in voteusers]
    if request.user in voteusers:
        voted = True
        return HttpResponseBadRequest("^_^")
    VoteUsers.objects.create(
        user=request.user,
        activity=activity,
        ph = ph)
    ph.votes = F('votes')+1
    ph.save()
    return HttpResponseRedirect(reverse('7show',args=[id]))
    
  
def deletework(request,id):
    photo = get_object_or_404(Photograph,id=id)
    if request.user.id !=photo.author.id:
        raise Http404()

    index = photo.index
    activity = photo.activity
    for file in [photo.path,photo.thumb128,photo.thumb64]:
        cmd = 'rm ' + MEDIA_ROOT + file
        os.system(cmd)
    photo.delete()
    if index != activity.photo_num:
        num = gallery.photo_num
        for i in range(index,num+1):
            activity.photograph_set.filter(index=i).update(index=F('index')-1)

    activity.photo_num=F('photo_num')-1
    activity.save()
    activity = Activity.objects.get(pk=activity.pk)
    
    return HttpResponseRedirect(reverse('7activity',args=[activity.id]))
    
def show(request,id):
    photo = get_object_or_404(Photograph,id=id)
    people = photo.author
    activity = photo.activity

    OTHER = True if people.id != request.user.id else False
    voteusers = VoteUsers.objects.filter(ph = photo)
    voteusers = [vu.user for vu in voteusers]
   
    if request.user in voteusers:
        voted = True
    if activity.end_date < timezone.now().date():
        exceed = True

    if people.id != request.user.id:
        neighbour = 1
        #if people not in my circle's left friend,eyeon him
        try:
            my_circle = Circle.objects.get(user_id=request.user.id)
        except:
            neighbour_off = 1
        else:
            if not my_circle.leftright_set.filter(friend=people,friend_type="left"):
                neighbour_off = 1

    
    p,n = photo.index-1,photo.index+1
    if p < 1:
        p = activity.photo_num
    if n > activity.photo_num:
        n = 1
    pp = Photograph.objects.filter(activity_id = activity.id).get(index=p)
    np = Photograph.objects.filter(activity_id = activity.id).get(index=n)

   
    return render_to_response('activity/show.html',
                              locals(),
                              RequestContext(request))
    


@login_required
def anticipate(request,activity_id):
    if request.method != 'POST' or request.FILES == None or 'work' not in request.FILES:
        return HttpResponseBadRequest('must choose a photo')

    id = int(activity_id)
    activity = get_object_or_404(Activity,id=id)
    photos = Photograph.objects.filter(activity_id=id)
    authors=[photo.author for photo in photos]
    if request.user in authors:
        participanted = True
        return HttpResponseBadRequest('^-^')

    ufile = request.FILES['work']    
    parent = str(id/10000)
    child = str(id%10000)

    path = '/'.join(['activity',parent,child])

    fold = os.path.join(MEDIA_ROOT,path)
    filename = str(random.randint(1,1000))+'_'+ufile.name
    filepath = path+filename
    thumbpath = filepath + '.thumbnail'
    thumbpath2 = thumbpath+'2'
    
    if not os.path.exists(fold):
        os.makedirs(fold)   

    try:
        image = Image.open(ufile)
    except:
        return HttpResponseBadRequest("请选择正确的图片参加活动")
    image.save(os.path.join(MEDIA_ROOT,filepath))
    image.thumbnail((128,128),Image.ANTIALIAS) 
    image.save(os.path.join(MEDIA_ROOT,thumbpath),'JPEG')
    image.thumbnail((64,64),Image.ANTIALIAS)
    image.save(os.path.join(MEDIA_ROOT,thumbpath2),'JPEG')

    activity.photo_num = F('photo_num')+1
    activity.save()
    activity = Activity.objects.get(pk=activity.pk)
    index = activity.photo_num
    print 'create before:',index
    pg = Photograph.objects.create(
        activity = activity,
        author = request.user,
        index = index,
        name = filename,
        path = filepath,
        thumb128 = thumbpath,
        thumb64 = thumbpath2)
    
    VoteUsers.objects.create(
        user=request.user,
        activity=activity,
        ph = pg)

    PartSaying.objects.create(
        user = request.user,
        activity = activity,
        work = pg,
        pub_date = timezone.now())

    return HttpResponseRedirect(reverse('7activity',args=[activity_id]))
    
