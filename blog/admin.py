from django.contrib import admin

from blog.models import Reaction,Sketch,Video, SketchThemes,VideoThemes,ReactThemes

# Register your models here.

admin.site.register(Reaction)

admin.site.register(Sketch)

admin.site.register(Video)

admin.site.register(ReactThemes)

admin.site.register(SketchThemes)

admin.site.register(VideoThemes)