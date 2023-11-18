from django.urls import path
from . import views
 
urlpatterns = [
    path("list/", views.MusicView.as_view(),name ='list'),
    path("user_playlists/", views.UserPlaylistsView.as_view(),name = 'user_playlists'),
    path('musics/<slug:pk>/', views.MusicDetailView.as_view(), name='music-detail'),
]
