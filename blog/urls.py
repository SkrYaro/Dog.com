from django.urls import path

from blog import views

urlpatterns = [
    path('',views.posts_list, name = 'main')
    ]