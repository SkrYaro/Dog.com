from django.urls import path

from chat import views

urlpatterns = [
    path("moderator/chat/" , views.chat, name="adminChat"),
    path("moderator/message/delete:<int:message_id>",views.delete,name ="mesDelete")
]