from django.urls import path

from blog import views,crud

urlpatterns = [
    path('',views.posts_list, name = 'main'),
    path('<str:post_type>',views.posts_list,name = "types_posts"),
    path("adminList/",views.adminList,name="moderatorList"),

    path('edit/post/<str:type>:id=<int:post_id>/user:<int:user_id>', crud.postEdit, name = "edit"),

    path('create/post/<str:type>', crud.postCreate ,name = "create"),

    path("delete/post/id=<int:post_id>" , crud.postDelete , name = "delete"),

    path("moderator/accept/post:<int:post_id>" , views.adminAccept ,name = "moderAccept"),
    path("moderator/delete/post:<int:post_id>" , views.adminDelete ,name = "moderDelete"),

    path("user/id:<int:user_id>", views.draftList , name = "drafts"),

    path("post/view/id=<int:post_id>" , views.postView , name = "post"),

    path("post/comment/add/post_id:<int:post_id>",crud.comentAdd, name = 'commentAdd'),

    path("post/comment/add/post_id:<int:post_id>/comment<int:comment_id>",crud.answerAdd, name = 'answerCommentAdd'),

    path("post/draft/accept/post:<int:post_id>", crud.postDraftConfirm , name = "draftConfirm"),

    path("profile/subscribe/user:<int:user_id>",crud.subscribe,name = "sub"),

    path("profile/unsubscribe/user:<int:user_id>",crud.desubscribe, name = 'desub'),

    path("post/subs/" ,views.postSubs, name = "subsPost"),

    path("profiles/",views.profilesList,name="profiles"),

    path("rate/<int:post_id>/<int:num>",crud.rate,name = "rate"),

    path("rate/del/<int:post_id>/", crud.deleteRating, name="delRate"),

    path("post/comment/delete/post_id:<int:post_id>/comment<int:comment_id>",crud.commentDelete, name = 'comDel'),

    path("subs/list/user:<int:user_id>/",views.subs,name = "subs"),

    #drf
    path("api/posts/", views.PostListAPI.as_view(), name="post-list-api")

]
