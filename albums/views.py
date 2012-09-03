# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse,Http404
from django.template.context import RequestContext
from albums.forms import CreateAlbum,UploadPhoto
from django.views.decorators.csrf import csrf_exempt
from albums.models import Gallery,Photo

from pk7lover.settings import MEDIA_ROOT,MEDIA_URL
import os
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

@csrf_exempt
def upload(request,album_id):
    if request.method != 'POST':
        return render_to_response('albums/upload.html',RequestContext(request))
    
    try:
        ufile = request.FILES['files[]']
    except:
        return render_to_response('albums/upload.html',RequestContext(request,{'upload_err':True}))

    id = int(album_id)
    parent = str(id/10000)
    child = str(id%10000)
    
    path = parent +'/' + child
    filename = str(random.randint(1,1000))+'_'+ufile.name
    filepath = os.path.join(MEDIA_ROOT,path,filename)
    thumbname = filepath + '.thumbnail'
    squarename = filepath + '.square'
    fold = os.path.join(MEDIA_ROOT,path)
    if not os.path.exists(fold):
        os.makedirs(fold)   
 
    image = Image.open(ufile)        
    image.save(filepath)
    image_square = image.resize((100,68),Image.ANTIALIAS)
    image_square.save(squarename,'JPEG')
    image.thumbnail((128,128),Image.ANTIALIAS) 
    image.save(thumbname,'JPEG')
    
    gallery = Gallery.objects.get(id=album_id)
    index = gallery.photo_num +1
    photo = Photo(gallery_id=album_id,
                  index = index,
                  name = filename,
                  thumbnail = thumbname.split('/')[-1],
                  parent = parent,
                  child = child)
    photo.save()
    gallery.photo_num = index
    gallery.save()

    return HttpResponseRedirect('../')
        
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
    
    



 
