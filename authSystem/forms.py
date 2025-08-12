from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, AbstractUser

from authSystem.models import CustomUser


class CustomCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("first_name",'last_name','email')