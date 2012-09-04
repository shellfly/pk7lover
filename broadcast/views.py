
from broadcast.models import Saying
from django.http import HttpResponseRedirect

# Create your views here.
def say(request):
    try: 
        text = request.POST['saying']
    except:
        print 'not saying'
    else:
        saying = Saying.objects.create(user=request.user,text=text)
       # saying.save()
    return HttpResponseRedirect('/')
