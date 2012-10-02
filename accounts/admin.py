from django.contrib import admin
from accounts.models import UserProfile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','activation_key','key_expires','was_expired')
    list_filter = ['key_expires']

admin.site.register(UserProfile,ProfileAdmin)
