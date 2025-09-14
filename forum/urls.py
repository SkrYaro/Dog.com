from django.urls import path

from forum import views

urlpatterns = [
    path("forum/", views.forum_view, name = "forum"),
    path("create/blank",views.blank_create,name = "blankCreate"),
    path("edit/blank<int:blank_id>",views.blank_edit,name= "editBlank"),
    path("view/blank<int:blank_id>",views.blank_view,name = "blank"),
    path("forum/draft/", views.draft_forum_view , name = "forumDraft"),
    path("accept/blank<int:blank_id>",views.blank_accept , name = "acceptBlank"),
    path("delete/blank<int:blank_id>",views.blank_delete, name = "deleteBlank"),

]