from django.db import models
from authSystem.models import Profile
# Create your models here.

def get_user_path(instanse , filename):
    ext = filename.split(".")[-1]
    return f'content/{instanse.contentMaker.user.username}.{ext}'


class Post(models.Model):
    name = models.CharField(max_length=50)
    contentImage = models.FileField(upload_to= get_user_path)
    description = models.CharField(max_length=500)
    contentMaker = models.ForeignKey(Profile, related_name='makerOfContent', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    time_add = models.DateTimeField(auto_now_add=True)
    time_upd = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.contentMaker}--->{self.name}'

