from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

from chat.forms import MessageForm
from chat.models import Message


# Create your views here.

def chat(request):
    messages = Message.objects.all()

    if request.method == "POST":
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user.user
            message.save()
            return redirect("adminChat")
    else:
        form = MessageForm()

    return render(request, template_name="admin/chat.html",context={"form":form,"chats":messages})

def delete(request , message_id):
    message = get_object_or_404(Message, id = message_id)
    if request.user == message.author.user:
        message.delete()
        return redirect("adminChat")
    else:
        raise PermissionDenied()


