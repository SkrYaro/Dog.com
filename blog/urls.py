from django.urls import path

from blog import views,crud

urlpatterns = [
    path('',views.posts_list, name = 'main'),

    path('reacts/', crud.reactiosnView, name='reactList'),
    path('reacts/create', crud.reactionCreate, name='reactCreate'),
    path('reacts/edit:<int:react_id>', crud.reactionEdit, name='reactEdit'),
    path('reacts/delete:<int:react_id>', crud.reactionDelete, name='reactDelete'),

    path('sketches/', crud.sketchesView, name='sketchesList'),
    path('sketches/create', crud.sketchCreate, name='sketchCreate'),
    path('sketches/edit:<int:sketch_id>', crud.sketchEdit, name='sketchEdit'),
    path('sketches/delete:<int:sketch_id>', crud.sketchDelete, name='sketchDelete'),

    path('videos/', crud.videosView, name='videosList'),
    path('videos/create', crud.videoCreate, name='videoCreate'),
    path('videos/edit:<int:video_id>', crud.videoEdit, name='videoEdit'),
    path('videos/delete:<int:video_id>', crud.videoDelete, name='videoDelete'),

    path("posts/video:<int:video_id>", crud.videoView , name = "videoPost"),
    path("posts/sketch:<int:sketch_id>", crud.sketchView , name = "sketchPost"),
    path("posts/reaction:<int:react_id>", crud.reactionView , name = "reactionPost"),
]
