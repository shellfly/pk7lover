# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from albums.forms import CreateAlbum
from albums.models import Gallery

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

def albums(request,username):
    return render_to_response('albums/albums.html',RequestContext(request,{}))

def album(request,username,album_id):
    pass


 
