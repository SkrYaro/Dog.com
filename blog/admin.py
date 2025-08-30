from django.contrib import admin

from blog.models import Post,Tags,Category

# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tags)
