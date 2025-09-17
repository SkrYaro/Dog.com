import random

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import Resolver404
from rest_framework.generics import ListCreateAPIView

from authSystem.models import Profile
from blog.forms import ComentCreateForm
from blog.models import Post, Comment, Sub, Category, Tag, Rating
from blog.serializers import PostSerializer


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
    name = request.GET.get("name")
    if name:
        profiles = profiles.filter(name__icontains=name)

    profiles = profiles.order_by("?")

    return render(request, "profiles/profiles.html", {"profiles": profiles})

def posts_list(request, post_type = None):
    posts = Post.objects.all()
    categories = Category.objects.all()
    tags_all = Tag.objects.all()  # всі теги

    new = request.GET.get("time_upd")
    if new:
        posts = posts.order_by("time_upd")

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

    posts = posts.annotate(average_rating=Avg("rating__rating"))

    rate = request.GET.get("rate")
    if rate:
        posts = posts.order_by("-average_rating")

    return render(
        request,
        template_name="blog/main_list.html",
        context={
            "posts": posts,
            "categories": categories,
            "tags": tags_all,               # всі теги для форми
            "selected_tags": selected_tags,
            "rate":rate
            # вибрані для збереження стану
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
    profile = get_object_or_404(Profile,id = request.user.id)
    post = get_object_or_404(Post,id = post_id)
    comments = Comment.objects.filter( post = post, answerOnYourself= None)
    form = ComentCreateForm()
    recs = recomend()
    try:
        rate = get_object_or_404(Rating, post=post, user=profile)
        rating = Rating.objects.filter(post=post).aggregate(Avg('rating'))['rating__avg']

        return render(request, template_name="blog/post.html",
                      context={"post": post, "form": form, "comments": comments, "recs": recs, "rating": rating,
                               "rate": rate})
    except:
        rating = Rating.objects.filter(post=post).aggregate(Avg('rating'))['rating__avg']

        return render(request, template_name="blog/post.html",context={"post":post,"form":form,"comments":comments,"recs":recs,"rating":rating})

def postSubs(request):
    profile = get_object_or_404(Profile , id = request.user.id)
    subs = list(Sub.objects.filter(fan = profile).values_list("author_id",flat=True))
    posts = Post.objects.filter(author_id__in = subs)

    categories = Category.objects.all()
    tags_all = Tag.objects.all()  # всі теги

    new = request.GET.get("time_upd")
    if new:
        posts = posts.order_by("time_upd")

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

    posts = posts.annotate(average_rating=Avg("rating__rating"))

    rate = request.GET.get("rate")
    if rate:
        posts = posts.order_by("-average_rating")




    return render(request, template_name="blog/main_list.html", context={"posts": posts,
            "categories": categories,
            "tags": tags_all,               # всі теги для форми
            "selected_tags": selected_tags,
            "rate":rate})

def fansList(request):
    profile = get_object_or_404(Profile, id = request.user.id)
    intoSub = len(list(Sub.objects.filter(fan=profile)))
    outoSub = len(list(Sub.objects.filter(author=profile)))

    return render(request, template_name="subs/subs_list.html", context={"intoSub":intoSub, "outoSub":outoSub})

def subs(request,user_id):
    profile = get_object_or_404(Profile, id = user_id)
    intoSubs = Sub.objects.filter(fan=profile)
    outoSubs = Sub.objects.filter(author=profile)

    return render(request, template_name="subs/subs_detail.html", context={"intosubs":intoSubs, "outosubs":outoSubs,"profile":profile})

class PostListAPI(ListCreateAPIView):
    queryset= Post.objects.all()
    serializer_class = PostSerializer