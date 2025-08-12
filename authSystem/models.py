from django.contrib.auth.models import User, AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from config import settings


# Create your models here.
def user_img_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'ava/{instance.user.username}.{ext}'


class Profile(models.Model):
    name = models.CharField(max_length=35, unique=True)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email = models.EmailField()
    bio = models.TextField()
    isOpen = models.BooleanField(default=False)
    isApplied = models.BooleanField(default=False)
    ava = models.ImageField(upload_to=user_img_path,default="media/ava/default.jpg")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    first_name =  models.CharField(max_length=35)
    last_name =  models.CharField(max_length=35)
    email = models.EmailField()

    def __str__(self):
        return self.first_name

class Subscribe(models.Model):
    creator = models.ForeignKey(Profile, related_name='contentMaker',on_delete=models.CASCADE)
    subscriber = models.ForeignKey(Profile, related_name='sub',on_delete=models.CASCADE)

    class Meta:
        pass

    def __str__(self):
        return self.creator.name

    def clean(self):
        if self.creator == self.subscriber:
            raise ValidationError('Сам на себе підписуватися не можна!')