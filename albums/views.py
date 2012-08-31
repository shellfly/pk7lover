# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from albums.forms import CreateAlbum,UploadPhoto
from django.views.decorators.csrf import csrf_exempt
from albums.models import Gallery,Photo

from pk7lover.settings import MEDIA_ROOT
import os
import random
from PIL import Image

def create(request):
    if request.method == 'POST':
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
            id = gallery.id
            return HttpResponseRedirect('/albums/%s/%d' % 
                                        (request.user.username,id))
    else:
        form = CreateAlbum(initial={'permission':'0'})
    return render_to_response('albums/create.html',RequestContext(request,{'form':form}))

def albums(request):
    albums = Gallery.objects.filter(user_id = request.user.id)
    print '%s has %d albums' % (request.user.username,albums.count())
    return render_to_response('albums/albums.html',RequestContext(request,locals()))


def album(request,username,album_id):
    parent = int(album_id) / 10000;
    child = int(album_id) % 10000;
    try:
        photos = Photo.objects.filter(gallery_id=album_id)
    except:
        photos = None
    return render_to_response('albums/album.html',
                              {'parent':parent,'child':child,'photos':photos},
                              RequestContext(request))

@csrf_exempt
def upload(request,album_id):
    id = int(album_id)
    parent = str(id/10000)
    child = str(id%10000)
    if request.method == 'POST':
        try:
            ufile = request.FILES['files[]']
        except:
            print 'file upload failed'
        else:
            image = Image.open(ufile)
            path = parent +'/' + child
            filename = str(random.randint(1,1000))+'_'+ufile.name
            thumbname = filename + '.thumbnail.jpg'
            fold = os.path.join(MEDIA_ROOT,path) 
            if not os.path.exists(fold):
                os.makedirs(fold)                
            image.save(os.path.join(fold,filename))
            image.thumbnail((128,128),Image.ANTIALIAS) 
            image.save(os.path.join(fold,thumbname))
            photo = Photo()
            photo.gallery_id = album_id;
            photo.name = filename
            photo.thumbnail = thumbname
            photo.parent = parent
            photo.child = child
            rand = random.randint(1,10000000)
            try:
                while Photo.objects.get(randomid=rand):
                    rand = random.randint(1,10000000)
            except:
                photo.randomid = rand
            photo.save()
            return HttpResponseRedirect('../')
    return render_to_response('albums/upload.html',RequestContext(request,{'album_id':id}))


def upload_image(request):
    path = request.path
    print path
    return HttpResponse("albums/upload")
  
def show_photo(request,id):
    try:
        photo = Photo.objects.get(randomid=id)
    except:
        pass

    return render_to_response('albums/show_photo.html',{'photo':photo},RequestContext(request))

def edit(request,album_id):
    pass

def order(request,album_id):
    pass


 
