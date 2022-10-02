from django.contrib import admin

from accounts.models import UserProfile, GroupProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(GroupProfile)