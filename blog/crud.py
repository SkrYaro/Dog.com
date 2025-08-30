from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from blog.forms import ReactCreateForm, SketchCreateForm, VideoCreateForm
from blog.models import Post , Tags,Category
from authSystem.models import Profile


def postCreate(request, type):
    profile = get_object_or_404(Profile, id = request.user.id)
    if request.method == "POST":
        match type:
            case "react":
                form = ReactCreateForm(request.POST)

                if form.is_valid():
                    react = form.save(commit=False)
                    react.author = profile
                    react.postType = type
                    react.save()
                    return redirect("drafts" ,request.user.id)
            case "video":
                form = VideoCreateForm(request.POST, request.FILES)
                if form.is_valid():
                    video = form.save(commit=False)
                    video.author = profile
                    video.postType = type
                    video.save()
                    return redirect("drafts",request.user.id)
            case "sketch":
                form = SketchCreateForm(request.POST, request.FILES)
                if form.is_valid():
                    sketch = form.save(commit=False)
                    sketch.author = profile
                    sketch.postType = "img"
                    sketch.save()
                    return redirect("drafts",request.user.id)
            case _ :
                raise ValueError("Post type error")

    else:
        match type:
            case "video":
                form = VideoCreateForm()
            case "sketch":
                form = SketchCreateForm()
            case "react":
                form = ReactCreateForm()
        return render(request, template_name="forms/formCreate.html", context={"form":form, "profile":profile ,"type":type})

def postEdit(request, type , post_id):
    profile = get_object_or_404(Profile, id=request.user.id)
    post = get_object_or_404(Post, id = post_id)
    if request.method == "POST":
        match type:
            case "react":
                form = ReactCreateForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.postType = type
                    post.author = profile
                    post.draft = False
                    post.save()
                    return redirect("main")
            case "video":
                form = VideoCreateForm(request.POST, request.FILES)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.author = profile
                    post.postType = type
                    post.draft = False
                    post.save()
                    return redirect("main")
            case "sketch":
                form = SketchCreateForm(request.POST, request.FILES)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.author = profile
                    post.postType = type
                    post.draft = False
                    post.save()
                    return redirect("main")
            case _:
                raise ValueError("Post type error")
    else:
        match type:
            case "video":
                form = VideoCreateForm(instance=post)
            case "sketch":
                form = SketchCreateForm(instance=post)
            case "react":
                form = ReactCreateForm(instance=post)
    return render(request, template_name="forms/formEdit.html", context={"form": form, "profile": profile, "post":post,"type":type})


def postDelete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author.user == request.user:
        post.delete()
        return redirect("drafts" ,request.user.id)
    else:
        raise PermissionDenied()

