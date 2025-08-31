from django.contrib import admin

from blog.models import Post, Tags, Category, Comment

# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tags)
admin.site.register(Comment)
