from django.contrib import admin

from blog.models import Post, Tag, Category, Comment, Sub

# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Sub)

