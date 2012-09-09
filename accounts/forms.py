# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _

class SignupForm(UserCreationForm):
    ''' 
    A form thats register a new user
    '''
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'duplicate_email':_("The email address has already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    
    email = forms.EmailField(label=_("E-mail"),max_length=40)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def save(self,commit=True):
        user = super(SignupForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = True;
        if commit:
            user.save();
        return user;
        
class ProfileFrom(forms.Form):
    nickname = forms.CharField(label=_("Nickname"),
                               max_length=7,
                               help_text='设置后可代替用户名在小7上显示')
    email = forms.EmailField(label=_("Email"),help_text="用于登陆或者密码重置")
    
