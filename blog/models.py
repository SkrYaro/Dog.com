from django.core.exceptions import ValidationError
from django.db import models
from authSystem.models import Profile
# Create your models here.

def get_user_path(instanse , filename):
    ext = filename.split(".")[-1]
    return f'img/{instanse.author.user.username}.{ext}'

def get_user_video_path(instanse , filename):
    ext = filename.split(".")[-1]
    return f'video/{instanse.author.user.username}.{ext}'

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Post(models.Model):
    types = (
        ("video","video"),
        ("react","react"),
        ("img","img")
    )
    postType = models.CharField(max_length=100,choices=types)
    name = models.CharField(max_length=50)
    video = models.FileField(upload_to=get_user_video_path, null=True, blank=True)
    img = models.ImageField(upload_to=get_user_path, null=True, blank=True)
    react = models.TextField(null=True, blank=True )
    description = models.TextField( )
    author = models.ForeignKey(Profile, related_name='posts', on_delete=models.CASCADE)
    draft = models.BooleanField(default=True )
    accepted = models.BooleanField(default=False)
    time_upd = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(Category,related_name="themes",on_delete=models.CASCADE, null=True,blank=True)
    tags = models.ManyToManyField(Tag, related_name="tags",blank=True)

class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Profile, related_name="comment", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="post", on_delete=models.CASCADE)
    answerOnYourself = models.ForeignKey("self",related_name="answer", on_delete=models.CASCADE, null=True,blank=True)

    time_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text} ---> {self.author.user}"



class Sub(models.Model):
    author = models.ForeignKey(Profile, related_name="maker", on_delete=models.CASCADE)
    fan = models.ForeignKey(Profile, related_name="fan" , on_delete=models.CASCADE)

    class Meta:
        unique_together = ("author","fan")
    def __str__(self):
        return f"{self.fan} ---> {self.author}"

    def clean(self):
        if self.author == self.fan:
            raise ValidationError("Ви не можете підписати на самого себе")


class Rating(models.Model):
    post = models.ForeignKey(Post,related_name="rating",on_delete=models.CASCADE)
    user = models.ForeignKey(Profile,related_name="owner",on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)

    def __str__(self):
        return {self.rating}

    def clean(self):
        if self.rating <= 0 or self.rating >5:
            raise ValidationError("Рейтинг має бути від 1 до 5")

