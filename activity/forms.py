from django.forms import ModelForm
from activity.models import Activity
from django.contrib import admin

class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        widgets={
            'beg_date':admin.widgets.AdminDateWidget,
            'end_date':admin.widgets.AdminDateWidget,
            }
        exclude = ('author')
