from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect

from panel.models import Speak, Dialog


def admin_list(request):
    if request.user.is_staff:
        chats = Dialog.objects.all()
        return render(request, template_name="admin/list.html", context={"chats": chats})
    else:
        raise PermissionDenied()

def dele(request,chat_id):
    chat = get_object_or_404(Dialog, id = chat_id)
    chat.delete()
    return redirect("adminReportList")

def del_messages(request,message_id,chat_id):
    mes = get_object_or_404(Dialog, id = message_id)
    if request.user.is_staff:
        mes.delete()
        return redirect("chat",chat_id)
    else:
        raise PermissionDenied()

