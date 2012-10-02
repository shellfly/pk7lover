from django.contrib import admin
from albums.models import Gallery,Photo

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('name','user','desc','comment','perm','create_date','was_created_recently')
    list_filter = ['create_date']
    date_hierarchy = 'create_date'

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('uname','gallery','desc','tags','upload_date','was_uploaded_recently')
    list_filter = ['upload_date']
    date_hierarchy = 'upload_date'

admin.site.register(Gallery,GalleryAdmin)
admin.site.register(Photo,PhotoAdmin)
