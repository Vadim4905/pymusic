from django.urls import path
from . import views
from django.views.i18n import JavaScriptCatalog




urlpatterns = [
    path('',  views.MusicListView.as_view(), name='index'),
    path('jsi18n', JavaScriptCatalog.as_view(), name='js-catlog'),
    path('artist/<uuid:pk>',views.ArtistDetailView.as_view(),name='artist-detail'),
    path('album/<uuid:pk>',views.AlbumDetailView.as_view(),name='album-detail'),
    path('music/<uuid:pk>', views.MusicDetailView.as_view(), name='music-detail'),
    path('artists/list',views.ArtistsListView.as_view(),name='artists-list'),
    path('artist/create',views.ArtistCreateView.as_view(),name='artist-create'),
    path('artist/<uuid:pk>/album/create',views.AlbumCreateView.as_view(),name='album-create'),
    path('album/<uuid:pk>/music/create',views.MusicCreateView.as_view(),name='music-create'),
    path('playlist/create',views.PlaylistCreateView.as_view(),name='playlist-create'),
    path('add-music-to-playlist/<uuid:music_id>/<uuid:playlist_id>/', views.add_music_to_playlist, name='add-music-to-playlist'),
    path('remove-music-from-playlist/<uuid:music_id>/<uuid:playlist_id>/', views.remove_music_from_playlist, name='remove-music-from-playlist'),
    path('playlist/<uuid:pk>',views.PlaylistDetailView.as_view(),name='playlist_detail'),
    path('search/', views.SearchResultsListView.as_view(), name='search_results'),
    
    path('download/<str:model_name>/<uuid:model_id>', views.BaseArchiveDownloadView.as_view(), name='download_archive'),
    



]