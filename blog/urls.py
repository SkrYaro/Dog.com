from django.urls import path

from blog import views,crud

urlpatterns = [
    path('',views.posts_list, name = 'main'),
    path("adminList/",views.adminList,name="moderatorList"),

    path('edit/post/<str:type>:id=<int:post_id>', crud.postEdit, name = "edit"),

    path('create/post/<str:type>', crud.postCreate ,name = "create"),

    path("delete/post/id=<int:post_id>" , crud.postDelete , name = "delete"),

    path("moderator/accept/post:<int:post_id>" , views.adminAccept ,name = "moderAccept"),
    path("moderator/delete/post:<int:post_id>" , views.adminDelete ,name = "moderDelete"),

    path("user/id:<int:user_id>", views.draftList , name = "drafts")
]
