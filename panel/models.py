from django.db import models
from authSystem.models import Profile
# Create your models here.

def message_img_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'message/{instance.user.username}.{ext}'
class Dialog(models.Model):
    title = models.CharField(max_length=100, default="Some problems")
    closed = models.BooleanField(default=False)
    user = models.ForeignKey(Profile, related_name="reporter",on_delete=models.CASCADE)
    time_start = models.DateTimeField(auto_now_add=True)
    time_end = models.DateTimeField(null=True,blank=True)

class Speak(models.Model):
    typeSpeak = (
        ("answer","answer"),
        ("ask","ask"),
    )
    speak = models.CharField(choices=typeSpeak ,max_length=100)
    user = models.ForeignKey(Profile, related_name="writer",on_delete=models.CASCADE)
    writes = models.TextField()
    image = models.ImageField(upload_to=message_img_path, null=True , blank=True)
    dialog = models.ForeignKey(Dialog, related_name="dialog" ,on_delete=models.CASCADE)





