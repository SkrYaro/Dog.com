from django.urls import path
from . import views
urlpatterns = [
    path('registration/',views.registration_view,name = 'register'),
    path('logout/', views.logout_view,name = 'logout'),
    path('login/',views.login_view, name = 'login'),
    path('profile/user:<int:user_id>/',views.Profiles.profile_view, name = 'profile'),
    path('profile/user:<int:user_id>/edit', views.Profiles.profile_edit, name='profileEdit'),
]