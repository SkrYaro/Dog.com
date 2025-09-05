import random

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import Resolver404

from authSystem.models import Profile
from blog.forms import ComentCreateForm
from blog.models import Post, Comment, Sub, Category, Tag


# Create your views here.
def recomend():
    recList = []
    posts = list(Post.objects.all())
    print(posts)
    random.shuffle(posts)
    for post in range(10):
        try:
            recList += posts[post]
        except:
            break

    return recList

def profilesList(request):
    profiles = Profile.objects.all()
    return render(request,template_name="profiles/profiles.html", context={"profiles":profiles})

def posts_list(request, post_type = None):
    posts = Post.objects.all()
    categories = Category.objects.all()
    tags_all = Tag.objects.all()  # всі теги

    if post_type:
        posts = posts.filter(postType = post_type)

    # Фільтр по категорії
    category = request.GET.get("category")
    if category:
        posts = posts.filter(category_id=category)
    name = request.GET.get("name")
    if name:
        posts = posts.filter(name__icontains=name)
    selected_tags = request.GET.getlist("tags")  # список вибраних id
    if selected_tags:
        posts = posts.filter(tags__in=selected_tags).distinct()


    return render(
        request,
        template_name="blog/main_list.html",
        context={
            "posts": posts,
            "categories": categories,
            "tags": tags_all,               # всі теги для форми
            "selected_tags": selected_tags  # вибрані для збереження стану
        }
    )
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
        raise PermissionDenied()


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
    recs = recomend()
    return render(request, template_name="blog/post.html",context={"post":post,"form":form,"comments":comments,"recs":recs})

def postSubs(request):
    profile = get_object_or_404(Profile , id = request.user.id)
    subs = list(Sub.objects.filter(fan = profile).values_list("author_id",flat=True))
    posts = Post.objects.filter(author_id__in = subs)
    return render(request, template_name="subs/sub_list.html", context={"posts":posts})

def fansList(request):
    profile = get_object_or_404(Profile, id = request.user.id)
    intoSub = len(list(Sub.objects.filter(fan=profile)))
    outoSub = len(list(Sub.objects.filter(author=profile)))

    return render(request, template_name="subs/subs_list.html", context={"intoSub":intoSub, "outoSub":outoSub})

