from django.contrib import admin
from activity.models import Activity,Photograph

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name','author','beg_date','end_date','tags','was_published_recently')
    list_filter = ['beg_date']
class PhotographAdmin(admin.ModelAdmin):
    list_display= ('name','author','desc','activity','join_date','was_published_recently')
    list_filter = ['join_date']
    date_hierarchy = 'join_date'

admin.site.register(Activity,ActivityAdmin)
admin.site.register(Photograph,PhotographAdmin)
