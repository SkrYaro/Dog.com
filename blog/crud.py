from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect

from blog.forms import ReactCreateForm, SketchCreateForm, VideoCreateForm
from blog.models import Video,Sketch,Reaction
from authSystem.models import Profile

def reactionView(request,react_id):
    react = get_object_or_404(Reaction, id = react_id)
    return render(request, template_name="forms/reactPost.html", context={"react":react})

def reactiosnView(request):
    reacts = Reaction.objects.all()
    return render(request, template_name="blog/reactList.html", context={"reacts":reacts})

def reactionCreate(request):
    profile = get_object_or_404(Profile, id = request.user.id)
    if request.method == "POST":
        form = ReactCreateForm(request.POST)
        if form.is_valid():
            react = form.save(commit=False)
            react.reactionMaker = profile
            react.save()
            return redirect("reactList")

    else:
        form = ReactCreateForm()
        return render(request, template_name = "forms/reactForm.html", context={"form":form,"profile":profile})


def reactionEdit(request, react_id):
    react = get_object_or_404(Reaction, id=react_id)
    if request.method == "POST":
        form = ReactCreateForm(request.POST, instance=react)
        if form.is_valid():
            form.save()
            return redirect("reactList")
    else:
        form = ReactCreateForm(instance=react)
        return render(request, template_name="forms/reactEditForm.html", context={"form": form,'react':react})


def reactionDelete(request,react_id):
    react = get_object_or_404(Reaction, id = react_id)
    if react.reactionMaker.user == request.user:
        react.delete()
        return redirect("reactList")
    else:
        raise PermissionDenied()


def sketchView(request, sketch_id):
    sketch = get_object_or_404(Sketch, id=sketch_id)
    return render(request, template_name="forms/sketchPost.html", context={"sketch": sketch})

def sketchesView(request):
    sketches = Sketch.objects.all()
    return render(request, template_name="blog/sketchesList.html", context={"sketches": sketches})

def sketchCreate(request):
    profile = get_object_or_404(Profile, id=request.user.id)
    if request.method == "POST":
        form = SketchCreateForm(request.POST, request.FILES)
        if form.is_valid():
            sketch = form.save(commit=False)
            sketch.sketchMaker = profile
            sketch.save()
            return redirect("sketchesList")

    else:
        form = SketchCreateForm()
        return render(request, template_name="forms/sketchForm.html", context={"form": form, "profile": profile})

def sketchEdit(request, sketch_id):
    sketch = get_object_or_404(Sketch, id=sketch_id)
    if request.method == "POST":
        form = SketchCreateForm(request.POST, request.FILES,instance=sketch)
        if form.is_valid():
            form.save()
            return redirect("sketchesList")
    else:
        form = SketchCreateForm(instance=sketch)
        return render(request, template_name="forms/sketchEditForm.html", context={"form": form, 'sketch': sketch})

def sketchDelete(request, sketch_id):
    sketch = get_object_or_404(Sketch, id=sketch_id)
    if sketch.sketchMaker.user == request.user:
        sketch.delete()
        return redirect("sketchesList")
    else:
        raise PermissionDenied()



def videoView(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, template_name="forms/videoPost.html", context={"video": video})

def videosView(request):
    videos = Video.objects.all()
    return render(request, template_name="blog/videosList.html", context={"videos": videos})

def videoCreate(request):
    profile = get_object_or_404(Profile, id=request.user.id)
    if request.method == "POST":
        form = VideoCreateForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.videoMaker = profile
            video.save()
            return redirect("videosList")

    else:
        form = VideoCreateForm()
        return render(request, template_name="forms/videoForm.html", context={"form": form, "profile": profile})

def videoEdit(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == "POST":
        form = VideoCreateForm(request.POST, request.FILES,instance=video)
        if form.is_valid():
            form.save()
            return redirect("videosList")
    else:
        form = VideoCreateForm(instance=video)
        return render(request, template_name="forms/videoEditForm.html", context={"form": form, 'video': video})

def videoDelete(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if video.videoMaker.user == request.user:
        video.delete()
        return redirect("videosList")
    else:
        raise PermissionDenied()