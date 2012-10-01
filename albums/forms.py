from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

class CreateAlbum(forms.Form):
    RADIO=(('0',_('public')),('7',_('private')))
    name = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}),
                           max_length=90,
                           label=_('Album name'))
    permission = forms.ChoiceField(widget = forms.RadioSelect, 
                                   choices=RADIO,
                                   label=_('vpermission'))
    comment = forms.CharField(widget=forms.CheckboxInput(attrs={'name':'comment','value':'no'}),
                               label=_('No comment'))
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 7}),
                                  required=False,
                                 label=_('Album description'))

class UploadPhoto(forms.Form):
    pass

