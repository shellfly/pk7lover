# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse,Http404,HttpResponseBadRequest
from django.template.context import RequestContext
from albums.forms import CreateAlbum,UploadPhoto
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from albums.models import Gallery,Photo,user_modify_gallery,user_delete_photo
from broadcast.models import PhotoSaying as B_Photo
from pk7lover.settings import MEDIA_ROOT,MEDIA_URL

import os
import random
from PIL import Image

@login_required
def create(request):
    if request.method != 'POST':
        form = CreateAlbum(initial={'permission':'0'})
        return render_to_response('albums/create.html',RequestContext(request,{'form':form}))

    form = CreateAlbum(request.POST )
    if form.is_valid():
        cd = form.cleaned_data
        perm = int(cd['permission'])
        comm = False if cd['comment'] == 'no' else True
        gallery = Gallery.objects.create(user_id=request.user.id,
                          name=cd['name'],
                          desc=cd['description'],
                          perm=perm,
                          comment=comm)
        return HttpResponseRedirect('/albums/%s/%d' % 
                                    (request.user.username,gallery.id))
        

def show_photo(request,id):
    photo = get_object_or_404(Photo,id=id)
    album = photo.gallery
    album_id=album.id
    people = album.user
    
    OTHER = False 
    if not request.user.is_authenticated() or people.id != request.user.id:
        OTHER = True

    print album_id
    if album.perm != 0 and request.user.id != album.user_id:
        return render_to_response('albums/album.html',
                                  {'perm_err':True},
                                  RequestContext(request))

    p,n = photo.index-1,photo.index+1
    if p < 1:
        p = photo.gallery.photo_num
    if n > photo.gallery.photo_num:
        n = 1
    pp = Photo.objects.filter(gallery_id = photo.gallery_id).get(index=p)
    np = Photo.objects.filter(gallery_id = photo.gallery_id).get(index=n)
    return render_to_response('albums/show_photo.html',
                              locals(),
                              RequestContext(request))

from django.db import transaction

@transaction.autocommit
@csrf_exempt
@login_required
def upload(request,username,album_id=0):
    id = int(album_id)
    gallerys = Gallery.objects.filter(user_id=request.user.id)
    if request.method != 'POST':
        return render_to_response('albums/upload.html',RequestContext(request,locals()))
    
    if request.FILES == None:
        return HttpResponseBadRequest('Must have files attached!')
    if 'selected_album' not in request.POST:
        return HttpResponseBadRequest('Must select a album')

    ufile = request.FILES[u'files[]']
    id = int(request.POST['selected_album'])
    parent = str(id/10000)
    child = str(id%10000)
    
    path = parent +'/' + child + '/'
    fold = os.path.join(MEDIA_ROOT,path)
    filename = str(random.randint(1,1000))+'_'+ufile.name
    filepath = path+filename
    thumbpath = filepath + '.thumbnail'
    thumbpath2 = thumbpath+'2'
    squarepath = filepath + '.square'
   
    if not os.path.exists(fold):
        os.makedirs(fold)   
    
    image = Image.open(ufile)        
    image.save(os.path.join(MEDIA_ROOT,filepath))
    print 'hello'
    image_square = image.resize((100,100),Image.ANTIALIAS)
    image_square.save(os.path.join(MEDIA_ROOT,squarepath),'JPEG')
    image.thumbnail((128,128),Image.ANTIALIAS) 
    image.save(os.path.join(MEDIA_ROOT,thumbpath),'JPEG')
    image.thumbnail((64,64),Image.ANTIALIAS)
    image.save(os.path.join(MEDIA_ROOT,thumbpath2),'JPEG')
    print 'hello2'
    gallery = Gallery.objects.select_for_update().get(id=album_id)
    gallery.photo_num = F('photo_num')+1
    gallery.save()
    gallery = Gallery.objects.get(pk=gallery.pk)
    index = gallery.photo_num
   
   
    Photo.objects.create(gallery_id=album_id,
                         index = index,
                         name = filename,
                         path = filepath,
                         thumb128 = thumbpath,
                         thumb64 = thumbpath2,
                         square = squarepath)

    user_modify_gallery.send(sender=Photo,gallery=gallery)
    if not gallery.cover:
        gallery.cover = squarepath
        gallery.save()

    b_photos = B_Photo.objects.filter(gallery_id=album_id).order_by('-pub_date') 
    if b_photos.count() != 0 and b_photos[0].pub_date.strftime("%Y%m%d") == timezone.now().strftime("%Y%m%d"):
        b_photo = b_photos[0]
    else:
        b_photo = B_Photo.objects.create(user_id=request.user.id,gallery_id=album_id)
        
    b_photo.num = F('num')+1
    b_photo.pub_date = timezone.now()
    b_photo.save()
 
    from django.utils import simplejson
    result = []
    result.append({"name":filename, 
                   "size":ufile.size, 
                   "url":MEDIA_URL+filepath, 
                   "thumbnail_url":MEDIA_URL+thumbpath,
                   "delete_url":'', 
                   "delete_type":"POST",})
    response_data = simplejson.dumps(result)

    if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
        mimetype = 'application/json'
    else:
        mimetype = 'text/plain'
    return HttpResponse(response_data, mimetype=mimetype)
 
@login_required       
def edit(request,album_id):
    pass

@login_required
def order(request,album_id):
    pass


def album(request,username,album_id):
    people = get_object_or_404(User,username=username)
    try:
        album = people.gallery_set.get(id=album_id)
    except:
        return HttpResponseBadRequest('%s don\'t have this album' % people.username)

    OTHER = False
    if not request.user.is_authenticated() or request.user.id !=people.id:
        OTHER = True   

    if album.perm != 0 and OTHER:
        return render_to_response('albums/album.html',
                                  {'perm_err':True},
                                  RequestContext(request)) 
    try:
        photos = Photo.objects.filter(gallery_id=album_id)
    except:
        photos = None
    return render_to_response('albums/album.html',
                              locals(),
                              RequestContext(request))

def albums(request,username):
    people = get_object_or_404(User,username=username)
    albums = Gallery.objects.filter(user_id = people.id)
    OTHER = False
    if not request.user.is_authenticated() or request.user.id !=people.id:
        OTHER = True
    return render_to_response('albums/albums.html',RequestContext(request,locals()))

@login_required
def setcover(request,id):
    photo = get_object_or_404(Photo,id=id)
    cover_url = photo.square
    gallery = photo.gallery
    gallery.cover = cover_url
    gallery.save()
    return HttpResponseRedirect(reverse('7single_photo',args=[photo.id]))
    
    
@login_required
def del_album(request,username,album_id):
    people =  get_object_or_404(User,username=username)

    OTHER = False
    if not request.user.is_authenticated() or request.user.id !=people.id:
        OTHER = True 
    if not OTHER:
        Gallery.objects.get(id=album_id).delete()
    return HttpResponseRedirect(reverse('7albums',args=[username]))
    
@login_required
def del_photo(request,photo_id):
    photo = Photo.objects.get(id=photo_id)
    index = photo.index
    gallery = photo.gallery
    photo.delete()
    print 'delete' + photo.name
    user_delete_photo.send(sender=Photo,gallery=gallery,index=index)
    try:
        photo = gallery.photo_set.get(index=index)
    except:
        return HttpResponseRedirect(reverse('7single_album',args=[request.user.username,gallery.id]))
    
    return HttpResponseRedirect(reverse('7single_photo',args=[photo.id]))
    

 
