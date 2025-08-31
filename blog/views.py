from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import Resolver404

from authSystem.models import Profile
from blog.forms import ComentCreateForm
from blog.models import Post, Comment


# Create your views here.

@login_required
def posts_list(request):

    posts = Post.objects.all()

    return render(request, template_name="blog/main_list.html", context={"posts":posts})

def draftList(request, user_id):
    profile = get_object_or_404(Profile , id = user_id)
    if profile.user == request.user:
        posts = Post.objects.filter(author = profile)
        return render(request,template_name="profiles/yourPost.html", context={"profile":profile,"posts":posts})
    else:
        raise PermissionDenied()

def adminList(request):
    if request.user.is_staff:
        posts = Post.objects.all()
        return render(request, template_name="admin/adminList.html", context={"posts": posts})
    else:
        raise Resolver404()

def adminAccept(request, post_id):
    post = get_object_or_404(Post, id = post_id)

    if request.user.is_staff:
        post.accepted = True
        post.save()
        return redirect("moderatorList")
    else:
        raise Resolver404()


def adminDelete(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user.is_staff:
        post.delete()
        return redirect("moderatorList")
    else:
        raise PermissionDenied()

def postView(request, post_id):
    post = get_object_or_404(Post,id = post_id)
    comments = Comment.objects.filter( post = post, answerOnYourself= None)
    form = ComentCreateForm()
    return render(request, template_name="blog/post.html",context={"post":post,"form":form,"comments":comments})
