from django.contrib.auth.decorators import login_required
from django.contrib.messages.context_processors import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from blog.forms import ReactCreateForm, SketchCreateForm, VideoCreateForm, ComentCreateForm
from blog.models import Post, Tag, Category, Comment, Sub, Rating
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
                    form.save_m2m()
                    return redirect("drafts" ,request.user.id)
            case "video":
                form = VideoCreateForm(request.POST, request.FILES)
                if form.is_valid():
                    video = form.save(commit=False)
                    video.author = profile
                    video.postType = type
                    video.save()
                    form.save_m2m()
                    return redirect("drafts",request.user.id)
            case "sketch":
                form = SketchCreateForm(request.POST, request.FILES)
                if form.is_valid():
                    sketch = form.save(commit=False)
                    sketch.author = profile
                    sketch.postType = "img"

                    sketch.save()
                    form.save_m2m()
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

def postEdit(request, type , post_id,user_id):
    profile = get_object_or_404(Profile, id=user_id)
    post = get_object_or_404(Post, id = post_id)
    if request.user == profile.user or request.user.is_staff:
        if request.method == "POST":
            match type:
                case "react":
                    form = ReactCreateForm(request.POST,instance=post)
                case "video":
                    form = VideoCreateForm(request.POST, request.FILES,instance=post)
                case "img":
                    form = SketchCreateForm(request.POST, request.FILES,instance=post)

                case _:
                    raise ValueError("Post type error")
            if form.is_valid():
                post = form.save(commit=False)
                post.author = profile
                post.postType = type
                post.accepted = False
                if request.user.is_staff:
                    post.accepted = True
                    post.save()
                    form.save_m2m()
                    return redirect("moderatorList")
                else:
                    post.save()
                    form.save_m2m()
                    return redirect("drafts", request.user.id)

        else:
            match type:
                case "video":
                    form = VideoCreateForm(instance=post)
                case "img":
                    form = SketchCreateForm(instance=post)
                case "react":
                    form = ReactCreateForm(instance=post)
                case _:
                    raise ValueError("Post type error")

        return render(request, template_name="forms/formEdit.html", context={"form":form, "profile": profile, "post":post,"type":type})
    else:
        raise PermissionDenied()

def postDelete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author.user == request.user:
        post.delete()
        return redirect("drafts" ,request.user.id)
    else:
        raise PermissionDenied()

def postDraftConfirm(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    if post.author.user == request.user:
        post.draft = False
        post.save()
        return redirect("drafts", request.user.id)
    else:
        raise PermissionDenied()

def comentAdd(request,post_id):
    profile = get_object_or_404(Profile, id = request.user.id)
    post = get_object_or_404(Post,id = post_id)
    if request.method == "POST":
        form = ComentCreateForm(request.POST)
        if form.is_valid():
            coment = form.save(commit = False)
            coment.author = profile
            coment.post = post
            coment.save()
            return redirect("post", post.id)
    else:
        form = ComentCreateForm()
        return render(request,"blog/post.html", context={"form":form, "post":post})

def answerAdd(request, post_id,comment_id):
    profile = get_object_or_404(Profile, id = request.user.id)
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id = comment_id)
    if request.method == "POST":
        form = ComentCreateForm(request.POST)
        if form.is_valid():
            coment = form.save(commit=False)
            coment.author = profile
            coment.post = post
            coment.answerOnYourself = comment
            coment.save()
            return redirect("post", post.id)
    else:
        form = ComentCreateForm()
        return render(request, "blog/post.html", context={"form": form, "post": post, "comment":comment})


def subscribe(request, user_id):
    author = get_object_or_404(Profile, id = user_id)
    fan = get_object_or_404(Profile,id = request.user.id)
    try:
        get_object_or_404(Sub,author= author, fan=fan)
        return redirect("profile", user_id)
    except:
        sub = Sub.objects.create(
            author=author,
            fan=fan
        )
        sub.save()
        return redirect("profile", user_id)


def desubscribe(request, user_id):
    author = get_object_or_404(Profile, id=user_id)
    fan = get_object_or_404(Profile, id=request.user.id)
    try:
        unsub = get_object_or_404(Sub, author=author, fan=fan)
        unsub.delete()
        return redirect("profile", user_id)
    except:
        return redirect("profile", user_id)

def rate(request, post_id, num):
    post = get_object_or_404(Post, id = post_id)
    profile = get_object_or_404(Profile, id = request.user.id)

    try:
        rating = get_object_or_404(Rating, post = post, user=profile)
        rating.delete()
        rating = Rating.objects.create(post=post,user=profile,rating=num)
        rating.save()
    except:
        rating = Rating.objects.create(post=post,user=profile,rating=num)
        rating.save()
    return redirect("post",post_id)

def deleteRating(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    profile = get_object_or_404(Profile, id=request.user.id)
    try:
        rating = get_object_or_404(Rating, post = post, user=profile)
        rating.delete()
    except:
        pass
    return redirect("post",post_id)

def commentDelete(request, post_id,comment_id):
    coment = get_object_or_404(Comment,id = comment_id)
    post = get_object_or_404(Post, id = post_id)

    if request.user == (coment.author.user or post.author.user) or request.user.is_staff:
        coment.delete()
        return redirect("post",post_id)
    else:
        raise PermissionDenied()


