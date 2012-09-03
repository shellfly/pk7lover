# Create your views here.
import datetime,sha,random
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from django.template.response import TemplateResponse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as auth_login,logout as auth_logout,REDIRECT_FIELD_NAME
from django.contrib.sites.models import get_current_site

from accounts.models import UserProfile
from django.utils.encoding import smart_str
from django.contrib.auth.forms import AuthenticationForm

from django.core.mail import send_mail
from albums.models import Gallery
from accounts.forms import SignupForm


@login_required
def profile(request):
    albums = Gallery.objects.filter(user_id=request.user.id)
    return render_to_response('accounts/profile.html',RequestContext(request,locals()))


def login(request,template_name='accounts/login.html',
          authentication_form=AuthenticationForm,
          redirect_field_name = REDIRECT_FIELD_NAME,
          current_app=None):

    redirect_to = request.GET[redirect_field_name] if request.GET.has_key(redirect_field_name) else '/'

    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect_to)
    if request.method == 'POST':
        form = authentication_form(data = request.POST)
        if form.is_valid():
            auth_login(request,form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponseRedirect(redirect_to)
        else:
            return render_to_response(template_name,RequestContext(request,{'form':form}))
    else:
        form = authentication_form(request)
    
    request.session.set_test_cookie()
    current_site = get_current_site(request)
    context = {'form':form,
               'site':current_site,
               'site_name':current_site.name,}
    return TemplateResponse(request,template_name,context,current_app=current_app)
    
def logout(request,redirect_field_name = REDIRECT_FIELD_NAME):
    redirect_to = request.GET[redirect_field_name] if request.GET.has_key(redirect_field_name) else '/'
    auth_logout(request)
    return HttpResponseRedirect(redirect_to)


def check_email(user):
    salt = sha.new(str(random.random())).hexdigest()[:5]
    activation_key = sha.new(salt+user.username).hexdigest()
    key_expires = datetime.datetime.today() + datetime.timedelta(2)
    new_profile = UserProfile(user=user,activation_key=activation_key,key_expires=key_expires)
    new_profile.save()
    email_subject = 'Your new pk7lover.net account confirmation'
    email_body = '''Hello, %s, and thanks for signing up for an        
pk7lover.com account!\n\nTo activate your account, click this link within 48 
hours:\n\nhttp://localhost:8000/accounts/confirm/%s''' % (
                user.username,
                new_profile.activation_key)
    send_mail(email_subject,
              email_body,
              'shell0fly@gmail.com',
              [user.email])
    
def signup(request,usercreation_form=SignupForm): 
    if request.method == 'POST':
        form = usercreation_form(data = request.POST)
        if form.is_valid():
            user = form.save();
            #check_email(user)
            return render_to_response('accounts/signup.html',
                                      RequestContext(request,{'submitinfo':True,'form':form}))
    else:
        form = usercreation_form()

    return render_to_response('accounts/signup.html',RequestContext(request,{'form':form}))


def confirm(request,activation_key):
    if request.user.is_authenticated():
        return render_to_response('confirm.html', {'has_account': True})
    user_profile = get_object_or_404(UserProfile,
                                     activation_key=activation_key)
    if user_profile.key_expires < datetime.datetime.today():
        return render_to_response('confirm.html', {'expired': True})
    user_account = user_profile.user
    user_account.is_active = True
    user_account.save()
    return render_to_response('confirm.html', {'success': True})


def people(request,username):
    people = get_object_or_404(User,username=username)
    albums = Gallery.objects.filter(user_id=people.id)
    return render_to_response('accounts/member.html',RequestContext(request,locals()))
