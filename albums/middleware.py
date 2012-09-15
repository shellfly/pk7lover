from django.conf import settings

class UploadifyMiddleware(object):
    def process_request(self,request):
        if request.method == 'POST' and request.POST.has_key('upload_sessionid'):
            request.COOKIES[settings.SESSION_COOKIE_NAME] = request.POST['upload_sessionid']
            #request.COOKIES['csrftoken'] = request.POST['csrftoken']
