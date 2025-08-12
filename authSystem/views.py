from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CustomCreateForm
from .models import Profile

# Create your views here.

def registration_view(request):
    if request.method == "POST":
        form = CustomCreateForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request,user)
            Profile.objects.create(
                name = user.username,
                bio = "zero bio",
                user = user
            )
            return redirect('login')
    else:
        form = CustomCreateForm()
    return render(request, template_name="auth/register.html", context={'form':form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('login')
            return render(request, "auth/login.html", context={"form": form})
    else:
        form = AuthenticationForm()
    return render(request,"auth/login.html",context={"form":form})

def logout_view(request):
    logout(request)
    return redirect("login")

class Profiles:
    home = 'profile'

    def profile_view(request, user_id):
        profile = get_object_or_404(Profile,id = user_id)

        return render(request,template_name='profiles/profile.html', context={'profile':profile})






