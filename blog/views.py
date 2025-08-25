from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from blog.models import Reaction, Sketch, Video


# Create your views here.

@login_required
def posts_list(request):

    posts = []
    react = Reaction.objects.all()
    posts += react
    sketches = Sketch.objects.all()
    posts += sketches
    videos = Video.objects.all()
    posts += videos

    return render(request, template_name="blog/main_list.html", context={"posts":posts})
