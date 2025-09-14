from django.db import models

from authSystem.models import Profile


# Create your models here.

def get_admin_img(instanse , filename):
    ext = filename.split(".")[-1]
    return f'adminChat/{instanse.author.user.username}.{ext}'

class Message(models.Model):
    text = models.TextField()
    img = models.ImageField(upload_to=get_admin_img, null=True,blank=True)
    author = models.ForeignKey(Profile, related_name="message", on_delete=models.CASCADE )
    time_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} ---> {self.text}  --- {self.time_add}"


