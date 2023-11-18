from django.urls import path
from . import views
from django.views.i18n import JavaScriptCatalog




urlpatterns = [
    path('',  views.IndexView.as_view(), name='index'),
    path('jsi18n', JavaScriptCatalog.as_view(), name='js-catlog'),
    path('artist/<uuid:pk>',views.ArtistView.as_view(),name='artist_detail'),
    path('album/<uuid:pk>',views.AlbumView.as_view(),name='album_detail'),
    path('music/<uuid:pk>', views.MusicView.as_view(), name='music_detail'),
    path('artists/list',views.ArtistsList.as_view(),name='artists_list'),
    path('artist/create',views.ArtistCreateView.as_view(),name='artist_create'),
    path('artist/<uuid:pk>/album/create',views.AlbumCreateView.as_view(),name='album_create'),
    path('album/<uuid:pk>/music/create',views.MusicCreateView.as_view(),name='music_create'),
    path('playlist/create',views.PlaylistCreateView.as_view(),name='playlist_create'),
    path('add_music_to_playlist/<uuid:music_id>/<uuid:playlist_id>/', views.add_music_to_playlist, name='add_music_to_playlist'),
    path('remove_music_from_playlist/<uuid:music_id>/<uuid:playlist_id>/', views.remove_music_from_playlist, name='remove_music_from_playlist'),
    path('playlist/<uuid:pk>',views.PlaylistView.as_view(),name='playlist_detail'),
    path('search/', views.SearchResultsListView.as_view(), name='search_results'),
    path('download_album_archive/<uuid:model_id>', views.ArchiveDownloadAlbumView.as_view(), name='download_album'),
    path('download_artist_archive/<uuid:model_id>', views.ArchiveDownloadArtistView.as_view(), name='download_artist'),
    path('download_playlist_archive/<uuid:model_id>', views.ArchiveDownloadPlaylistView.as_view(), name='download_playlist'),



]