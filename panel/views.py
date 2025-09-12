from datetime import timezone

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models.functions import datetime
from django.shortcuts import render, get_object_or_404, redirect

from authSystem.models import Profile
from panel.forms import MessageForm, DialogForm
from panel.models import Speak, Dialog


# Create your views here.
@login_required
def chat_list(request, user_id):
    profile = get_object_or_404(Profile,id = user_id)
    chats = Dialog.objects.filter(user = profile)
    return render(request, template_name="report/list.html", context={"chats": chats})



def chat(request , chat_id):
    chat = get_object_or_404(Dialog, id = chat_id)
    profile = get_object_or_404(Profile , user = request.user)
    if chat.user.user == request.user or request.user.is_staff:
        try:
            speaks = Speak.objects.filter(dialog=chat)
        except:
            speaks = None
        if not chat.closed:
            if request.method == "POST":
                form = MessageForm(request.POST, request.FILES)
                if form.is_valid():
                    message = form.save(commit=False)
                    message.user = profile
                    message.dialog = chat
                    if request.user.is_staff and chat.user.user != request.user:
                        message.speak = "answer"
                    elif chat.user.user  == request.user:
                        message.speak = "ask"
                    else:
                        message.speak = "ask"
                    message.save()
                return redirect("reportChat",chat_id)
            else:
                form = MessageForm()
            return render(request,template_name="report/chat.html",context={"form":form,"chat":chat,"speaks":speaks})
        else:
            return render(request,template_name="report/chat.html",context={"chat":chat,"speaks":speaks})

    else:
        raise PermissionDenied()


def close(request,chat_id):
    chat = get_object_or_404(Dialog, id = chat_id)
    chat.closed = True
    chat.time_end = datetime.timezone.now()
    chat.save()
    return redirect("adminReportList")

def createReport(request):
    profile = get_object_or_404(Profile , id = request.user.id)
    if request.method == "POST":
        form = DialogForm(request.POST)
        first_com = MessageForm(request.POST, request.FILES)
        if form.is_valid() and first_com.is_valid():
            dialog = form.save(commit=False)
            dialog.user = profile
            comment = first_com.save(commit=False)
            comment.user = profile
            comment.speak = "ask"
            comment.dialog = dialog
            dialog.save()
            comment.save()
            return redirect("reportChat",dialog.id)
    else:
        form = DialogForm()
        first_com = MessageForm()
        return render(request,template_name="forms/reportForm.html",context={"form":form,"first_com":first_com})
