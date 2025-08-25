from django.db import models
from authSystem.models import Profile
# Create your models here.

def get_user_path(instanse , filename):
    ext = filename.split(".")[-1]
    return f'img/{instanse.sketchMaker.user.username}.{ext}'

def get_user_video_path(instanse , filename):
    ext = filename.split(".")[-1]
    return f'video/{instanse.videoMaker.user.username}.{ext}'

class Reaction(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    reactionMaker = models.ForeignKey(Profile, related_name='makerOfReaction', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    time_upd = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.reactionMaker}--->{self.name}'

class Video(models.Model):
    name = models.CharField(max_length=50)
    video = models.FileField(upload_to=get_user_video_path, )
    description = models.CharField(max_length=500)
    videoMaker = models.ForeignKey(Profile, related_name='makerOfVideo', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    time_upd = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.videoMaker}--->{self.name}'

class Sketch(models.Model):
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to=get_user_path)
    description = models.CharField(max_length=500)
    sketchMaker = models.ForeignKey(Profile, related_name='makerOfSketch', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    time_upd = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.sketchMaker}--->{self.name}'

class VideoThemes(models.Model):
    name = models.CharField(max_length=100)
    videoConnect = models.ForeignKey(Video, related_name="videoTheme", on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name}"


class SketchThemes(models.Model):
    name = models.CharField(max_length=100)
    sketchConnect = models.ForeignKey(Sketch, related_name="sketchTheme", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class ReactThemes(models.Model):
    name = models.CharField(max_length=100)
    reactConnect = models.ForeignKey(Reaction, related_name="videoTheme", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"
