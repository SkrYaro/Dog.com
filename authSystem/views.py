from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CustomCreateForm, CreateProfileForm
from .models import Profile

from blog.models import Sub
# Create your views here.

def registration_view(request):
    if request.method == "POST":
        form = CustomCreateForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request,user)
            Profile.objects.create(
                name = user.username,
                first_name = user.first_name,
                last_name = user.last_name,
                email = user.email,
                bio = "zero bio",
                user = user,
            )
            return redirect('profileEdit', request.user.id)
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
                return redirect('profile', request.user.id)
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
        intoSub = len(list(Sub.objects.filter(fan = profile)))
        outoSub = len(list(Sub.objects.filter(author = profile)))



        try:
            fan = get_object_or_404(Profile,id = request.user.id)
            subs = get_object_or_404(Sub , fan=fan,author = profile )
            sub = True
        except:
            sub = False

        return render(request,template_name='profiles/profile.html', context={'profile':profile, "sub":sub,"intoSub":intoSub,"outoSub":outoSub})
    @login_required

    def profile_edit(request, user_id):
        profile = get_object_or_404(Profile, id = user_id)
        if request.user == profile.user or request.user.is_staff:
            if request.method == "POST":
                form = CreateProfileForm(request.POST, request.FILES, instance = profile)
                if form.is_valid():
                    form.save()
                    return redirect('profile',user_id)
                return render(request, 'profiles/profile_edit.html', context={'form': form, "profile": profile})

            else:
                form = CreateProfileForm(instance=profile)
            return render(request,'profiles/profile_edit.html',context={'form':form, "profile": profile})
        else:
            PermissionDenied()

