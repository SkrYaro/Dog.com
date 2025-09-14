from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect

from authSystem.models import Profile
from forum.forms import BlankForm
from forum.models import Forum


# Create your views here.

def forum_view(request):
    blanks = Forum.objects.all()

    return render(request,template_name="report/forum.html", context={"blanks":blanks})

def draft_forum_view(request):
    blanks = Forum.objects.all()

    return render(request, template_name="report/forumDraft.html", context={"blanks": blanks})


def blank_view(request, blank_id):
    blank = get_object_or_404(Forum, id = blank_id)

    return render(request,template_name="report/blank.html", context={"blank":blank})



def blank_create(request):
    profile = get_object_or_404(Profile , id = request.user.id)
    if request.user.is_staff:
        if request.method == "POST":
            form = BlankForm(request.POST, request.FILES)
            if form.is_valid():
                blank = form.save(commit = False)
                blank.author = profile
                blank.save()
                return redirect("forumDraft")
        else:
            form = BlankForm()
            return render(request,template_name="forms/blankForm.html",context={"form":form,"profile":profile})
    else:
        raise PermissionDenied()

def blank_edit(request,blank_id):
    blank = get_object_or_404(Forum, id = blank_id)
    if request.user.is_staff:
        if request.method == "POST":
            form = BlankForm(request.POST, request.FILES,instance=blank)
            if form.is_valid():
                blank = form.save(commit=False)
                blank.save()
                return redirect("forumDraft")
        else:
            form = BlankForm(instance=blank)
            return render(request, template_name="forms/editBlankForm.html", context={"form": form, "blank":blank})
    else:
        raise PermissionDenied()

def blank_delete(request,blank_id):
    blank = get_object_or_404(Forum, id = blank_id)
    if request.user.is_staff:
        blank.delete()
        return redirect("forumDraft")
    else:
        raise PermissionDenied()

def blank_accept(request,blank_id):
    blank = get_object_or_404(Forum, id = blank_id)
    if request.user.is_staff:
        blank.confirmed = True
        blank.save()
        return redirect("forumDraft")
    else:
        raise PermissionDenied()