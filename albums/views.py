# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse,Http404
from django.template.context import RequestContext
from albums.forms import CreateAlbum,UploadPhoto
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from albums.models import Gallery,Photo,user_modify_gallery
from broadcast.models import PhotoSaying as B_Photo

from pk7lover.settings import MEDIA_ROOT,MEDIA_URL
import os,datetime
import random
from PIL import Image

def create(request):
    if request.method != 'POST':
        form = CreateAlbum(initial={'permission':'0'})
        return render_to_response('albums/create.html',RequestContext(request,{'form':form}))

    form = CreateAlbum(request.POST )
    if form.is_valid():
        cd = form.cleaned_data
        perm = int(cd['permission'])
        comm = False if cd['comment'] == 'no' else True
        gallery = Gallery(user_id=request.user.id,
                          name=cd['name'],
                          description=cd['description'],
                          permission=perm,
                          comment=comm)
        gallery.save();
        return HttpResponseRedirect('/albums/%s/%d' % 
                                    (request.user.username,gallery.id))
        

def show_photo(request,id):
    photo = get_object_or_404(Photo,id=id)
    album = photo.gallery
    if album.permission != 0 and request.user.id != album.user_id:
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
                              {'photo':photo,'pp':pp,'np':np},
                              RequestContext(request))

from django.db import transaction

@transaction.autocommit
@csrf_exempt
def upload(request,username,album_id=0):
    from django.utils import simplejson
    if request.method != 'POST':
        return render_to_response('albums/upload.html',RequestContext(request,locals()))
    
    if request.FILES == None:
        return HttpResponseBadRequest('Must have files attached!')
    ufile = request.FILES[u'files[]']
    
    id = int(album_id)
    parent = str(id/10000)
    child = str(id%10000)
    
    path = parent +'/' + child
    filename = str(random.randint(1,1000))+'_'+ufile.name
    filepath = os.path.join(MEDIA_ROOT,path,filename)
    thumbpath = filepath + '.thumbnail'
    thumbpath2 = thumbpath+'2'
    squarepath = filepath + '.square'
    fold = os.path.join(MEDIA_ROOT,path)
    if not os.path.exists(fold):
        os.makedirs(fold)   
 
    image = Image.open(ufile)        
    image.save(filepath)
    image_square = image.resize((100,100),Image.ANTIALIAS)
    image_square.save(squarepath,'JPEG')
    image.thumbnail((128,128),Image.ANTIALIAS) 
    image.save(thumbpath,'JPEG')
    image.thumbnail((64,64),Image.ANTIALIAS)
    image.save(thumbpath2,'JPEG')
    
    gallery = Gallery.objects.select_for_update().get(id=album_id)
    index = gallery.photo_num+1
    
    Photo.objects.create(gallery_id=album_id,
                         index = index,
                         name = filename,
                         thumbnail = thumbpath.split('/')[-1],
                         thumbnail2 = thumbpath2.split('/')[-1],
                         parent = parent,
                         child = child)

    user_modify_gallery.send(sender=Photo,gallery=gallery)
    
    b_photos = B_Photo.objects.filter(gallery_id=gallery.id).order_by('-pub_date') 
    if b_photos.count() != 0 and b_photos[0].pub_date.strftime("%Y%m%d") == timezone.now().strftime("%Y%m%d"):
        b_photo = b_photos[0]
    else:
        b_photo = B_Photo.objects.create(user_id=request.user.id,gallery_id=gallery.id)

    b_photo.num = b_photo.num+1
    b_photo.pub_date = timezone.now()
    b_photo.save()
    gallery.photo_num = index
    gallery.save()

    result = []
    result.append({"name":filename, 
                   "size":ufile.size, 
                   "url":MEDIA_URL+parent+'/'+child+'/'+filename, 
                   "thumbnail_url":MEDIA_URL+parent+'/'+child+'/'+thumbpath.split('/')[-1],
                   "delete_url":'', 
                   "delete_type":"POST",})
    response_data = simplejson.dumps(result)

    if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
        mimetype = 'application/json'
    else:
        mimetype = 'text/plain'
    return HttpResponse(response_data, mimetype=mimetype)
        
def edit(request,album_id):
    pass

def order(request,album_id):
    pass


def album(request,username,album_id):
    album = get_object_or_404(Gallery,id=album_id)

    if album.permission != 0 and request.user.id != album.user_id:
        return render_to_response('albums/album.html',
                                  {'perm_err':True},
                                  RequestContext(request)) 
    try:
        photos = Photo.objects.filter(gallery_id=album_id)
    except:
        photos = None
    return render_to_response('albums/album.html',
                              {'photos':photos},
                              RequestContext(request))

def albums(request):
    albums = Gallery.objects.filter(user_id = request.user.id)
    return render_to_response('albums/albums.html',RequestContext(request,{'albums':albums}))

def setcover(request,id):
    photo = get_object_or_404(Photo,id=id)
    cover_url = os.path.join(MEDIA_URL,photo.parent,photo.child,photo.name+'.square')
    gallery = photo.gallery
    gallery.cover = cover_url
    gallery.save()
    return HttpResponseRedirect("/albums/photos/%s" % id)
    
    



 
