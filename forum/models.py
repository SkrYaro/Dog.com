from django.db import models

from authSystem.models import Profile


# Create your models here.

def get_forum_img(instanse , filename):
    ext = filename.split(".")[-1]
    return f'adminChat/{instanse.author.user.username}.{ext}'

class Forum(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    img = models.ImageField(upload_to=get_forum_img,null=True,blank=True)
    confirmed = models.BooleanField(default=False)
    time_add = models.DateTimeField( auto_now_add=True)
    time_upd =models.DateTimeField( auto_now=True)
    author = models.ForeignKey(Profile , related_name="forums", on_delete=models.CASCADE)