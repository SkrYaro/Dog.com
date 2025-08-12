from django.contrib import admin
from django.contrib.auth.models import User

from .models import Profile, CustomUser, Subscribe
# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# class ProfileLine(admin.StackedInline):
#     model = Profile
#     can_delete = False
#     verbose_name_plural =  'profile'
#
# class UserAdmin(BaseUserAdmin):
#     inlines = [ProfileLine]


admin.site.register(CustomUser)

# admin.site.register(CustomUser)

admin.site.register(Profile)

admin.site.register(Subscribe)

