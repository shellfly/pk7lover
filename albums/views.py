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
    form = CreateAlbum(initial={'permission':'0'})
    if request.method == 'POST':
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
            return HttpResponseRedirect(reverse('7single_album',args=[gallery.id]))
    
    return render_to_response('albums/create.html',RequestContext(request,{'form':form}))

    

def show_photo(request,id):
    photo = get_object_or_404(Photo,id=id)
    album = photo.gallery
    album_id=album.id
    people = album.user
    
    OTHER = False 
    if not request.user.is_authenticated() or people.id != request.user.id:
        OTHER = True

    if album.perm != 0 and request.user.id != album.user_id:
        return render_to_response('albums/album.html',
                                  {'perm_err':True},
                                  RequestContext(request))

    p,n = photo.index-1,photo.index+1
    if p < 1:
        p = photo.gallery.photo_num
    if n > photo.gallery.photo_num:
        n = 1
    pp = Photo.objects.filter(gallery_id = album_id).get(index=p)
    np = Photo.objects.filter(gallery_id = album_id).get(index=n)
    return render_to_response('albums/show_photo.html',
                              locals(),
                              RequestContext(request))

@csrf_exempt
@login_required
def upload(request,album_id=0):

    id = int(album_id)
    upload_sessionid=request.COOKIES['sessionid']
    gallerys = Gallery.objects.filter(user_id=request.user.id)
    
    has_gallery = gallerys.count() > 0
    if not has_gallery:
        return HttpResponseRedirect(reverse('7create_album'))
    
    if request.method != 'POST':
        response=render_to_response('albums/upload.html',RequestContext(request,locals()))
        response.set_cookie('upload_sessionid',upload_sessionid,httponly=False)
        return response

    if request.FILES == None:
        return HttpResponseBadRequest('Must have files attached!')
    if 'selected_album' not in request.POST:
        return HttpResponseBadRequest('Must select a album')

    ufile = request.FILES[u'Filedata']
    id = int(request.POST['selected_album'])
    
    parent = str(id/10000)
    child = str(id%10000)
    
    print 'in  upload :'+ufile.name

    path = parent +'/' + child + '/'
    fold = os.path.join(MEDIA_ROOT,path)
    filename = str(random.randint(1,1000))+'_'+ufile.name
    filepath = path+filename
    thumbpath = filepath + '.thumbnail'
    thumbpath2 = thumbpath+'2'
    squarepath = filepath + '.square'
    
    if not os.path.exists(fold):
        os.makedirs(fold)   
    
    print 'in uplaod :'+path
    image = Image.open(ufile)        
    image.save(os.path.join(MEDIA_ROOT,filepath))
    
    image_square = image.resize((100,100),Image.ANTIALIAS)
    image_square.save(os.path.join(MEDIA_ROOT,squarepath),'JPEG')
    image.thumbnail((128,128),Image.ANTIALIAS) 
    image.save(os.path.join(MEDIA_ROOT,thumbpath),'JPEG')
    image.thumbnail((64,64),Image.ANTIALIAS)
    image.save(os.path.join(MEDIA_ROOT,thumbpath2),'JPEG')
    
    gallery = Gallery.objects.select_for_update().get(id=id)
    gallery.photo_num = F('photo_num')+1
    gallery.save()
    gallery = Gallery.objects.get(pk=gallery.pk)
    index = gallery.photo_num
    
    print 'in uplaod :'
    print index,gallery.photo_num
    photo = Photo.objects.create(gallery_id=id,
                                 index = index,
                                 name = filename,
                                 path = filepath,
                                 thumb128 = thumbpath,
                                 thumb64 = thumbpath2,
                                 square = squarepath)
    
    print 'after:',gallery.photo_num
    user_modify_gallery.send(sender=Photo,gallery=gallery)

    if not gallery.cover:
        gallery.cover = squarepath
        gallery.save()


    # update photo broadcast
    b_photos = B_Photo.objects.filter(gallery_id=id).order_by('-pub_date') 
    if b_photos.count() != 0 and b_photos[0].pub_date.strftime("%Y%m%d") == timezone.now().strftime("%Y%m%d"):
        b_photo = b_photos[0]
    else:
        b_photo = B_Photo.objects.create(user_id=request.user.id,gallery_id=id)
    
    b_photo.num = F('num')+1
    b_photo.pub_date = timezone.now()
    b_photo.save()  

    from django.utils import simplejson
    data = {'thumb64':photo.thumb64,'index':photo.index}
    return HttpResponse(simplejson.dumps(data))


@login_required
def edit(request,album_id):

    id = int(request.POST['album_id'])
    gallery = get_object_or_404(Gallery,pk=id,user=request.user)

    #cover is index of a photo
    if 'cover' in request.POST:
        cover_photo = gallery.photo_set.get(index=request.POST['cover'])
        gallery.cover = cover_photo.square
        gallery.save()
    [Photo.objects.filter(gallery_id=id,index=key).update(desc=request.POST[key])
     for key in request.POST.keys() if key.isdigit()] 
    return HttpResponseRedirect(reverse('7single_album',args=[id]))

@login_required
def property(request,album_id):
    pass

@csrf_exempt
def album(request,album_id):

    gallery = get_object_or_404(Gallery,id=album_id)
    people = gallery.user
    #OTHER is used in template,for identify 
    OTHER = False 
    if not request.user.is_authenticated() or request.user.id != people.id:
        OTHER = True   

    page = 1 if not 'p' in request.GET  else int(request.GET['p'])

    if gallery.perm != 0 and OTHER:
        return render_to_response('albums/album.html',
                                  {'perm_err':True},
                                  RequestContext(request)) 

    sum_pages = Photo.objects.filter(gallery_id=album_id).count() / 31
    pp,np = page-1,page+1
    photos = Photo.objects.filter(gallery_id=album_id)[(page-1)*30:page*30] #(page-1)*30:(page-1)*30+30
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
    if request.user.id !=photo.gallery.user.id:
        raise Http404()

    cover_url = photo.square
    gallery = photo.gallery
    gallery.cover = cover_url
    gallery.save()
    
    return HttpResponseRedirect(reverse('7single_album',args=[photo.gallery.id]))


@login_required
def del_album(request,album_id):
    gallery = get_object_or_404(Gallery,id=album_id)
    if  request.user.id !=gallery.user.id:
        raise Http404()
    
    gallery.delete()
    return HttpResponseRedirect(reverse('7albums',args=[people.username]))

@login_required
def del_photo(request,photo_id):
    photo = get_object_or_404(Photo,id=photo_id)
    if request.user.id !=photo.gallery.user.id:
        raise Http404()

    index = photo.index
    gallery = photo.gallery
    photo.delete()
    
    user_delete_photo.send(sender=Photo,gallery=gallery,index=index)
    if gallery.photo_num == 0:
        return HttpResponseRedirect(reverse('7single_album',args=[gallery.id]))

    #the photo be deleted is the last photo in gallery
    if index > gallery.photo_num:
        index = index-1
    photo = gallery.photo_set.get(index=index)
    return HttpResponseRedirect(reverse('7single_photo',args=[photo.id]))



