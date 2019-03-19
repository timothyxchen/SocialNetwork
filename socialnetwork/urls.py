from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.globalstream_action, name='home'),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
    path('globalstream', views.globalstream_action, name='globalstream'),
    path('add_post', views.add_post, name='add_post'),
    path('profile/<int:id>', views.profile_action, name='profile'),
    path('follow/<int:id>', views.follow_action, name='follow'),
    path('get_photo/<int:id>', views.get_photo, name='get_photo'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('followerstream', views.followerstream, name='followerstream'),

    path('add-comment', views.add_comment),
    path('refresh-global', views.refresh_global),
    path('refresh-follower', views.refresh_follower),
]

